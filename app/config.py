import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


DEBUG_RETRIEVAL = _env_bool("DEBUG_RETRIEVAL", True)

# 是否保存 AI 请求日志；生产环境建议关闭，避免持续写入用户问答。
ENABLE_PROMPT_LOG = _env_bool("ENABLE_PROMPT_LOG", True)
