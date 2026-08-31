import logging
import re
from time import perf_counter
from uuid import uuid4

from fastapi import Request


REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
access_logger = logging.getLogger("uvicorn.error.app_access")
access_logger.setLevel(logging.INFO)


def _request_id(value: str | None) -> str:
    if value and _REQUEST_ID_PATTERN.fullmatch(value):
        return value
    return str(uuid4())


async def observe_request(request: Request, call_next):
    """Attach a safe request ID and emit one privacy-conscious access log."""
    request_id = _request_id(request.headers.get(REQUEST_ID_HEADER))
    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        access_logger.exception(
            "request_failed request_id=%s method=%s path=%s "
            "status_code=500 duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    response.headers[REQUEST_ID_HEADER] = request_id
    access_logger.info(
        "request_complete request_id=%s method=%s path=%s "
        "status_code=%d duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response
