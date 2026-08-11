from collections import defaultdict


MAX_HISTORY_MESSAGES = 12

_sessions: dict[str, list[dict[str, str]]] = defaultdict(list)


def get_history(session_id: str) -> list[dict[str, str]]:
    """Return a copy of one conversation's recent messages."""

    return list(_sessions.get(session_id, []))


def append_exchange(session_id: str, question: str, answer: str) -> None:
    """Store one user/assistant exchange and keep the context bounded."""

    history = _sessions[session_id]
    history.extend(
        [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    )
    _sessions[session_id] = history[-MAX_HISTORY_MESSAGES:]


def clear_history(session_id: str) -> None:
    """Clear a conversation without affecting other sessions."""

    _sessions.pop(session_id, None)
