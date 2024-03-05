from contextvars import ContextVar
from typing import Union

from sqlalchemy.orm import Session

_session: ContextVar[Union[Session, None]] = ContextVar("_session", default=None)


def get_session() -> Session:
    """Returns the current session."""
    session = _session.get()

    if session is None:
        raise RuntimeError("No session is available")

    return session
