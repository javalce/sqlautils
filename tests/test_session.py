from sqlalchemy.orm import Session
from sqlautils.session import _session, get_session


def test_get_session():
    # Test when session is available
    session = Session()
    _session.set(session)
    assert get_session() == session

    # Test when session is not available
    _session.set(None)
    try:
        get_session()
        raise AssertionError("Expected RuntimeError")
    except RuntimeError as e:
        assert str(e) == "No session is available"
