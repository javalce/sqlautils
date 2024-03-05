from sqlalchemy.orm import Session
from sqlautils.session import _session, get_session


def test_get_session_when_available():
    session = Session()
    _session.set(session)
    assert get_session() == session


def test_get_session_when_not_available():
    _session.set(None)
    try:
        get_session()
    except RuntimeError as e:
        assert str(e) == "No session is available"
