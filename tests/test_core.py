import pytest
from sqlautils.core import SQLADatabase


def test_sqladatabase_init():
    db = SQLADatabase(url="sqlite:///:memory:")
    assert db.url == "sqlite:///:memory:"


def test_sqladatabase_initialize():
    db = SQLADatabase()
    with pytest.raises(ValueError):
        db.initialize(url=None)
    db.initialize(url="sqlite:///:memory:")
    assert db.url == "sqlite:///:memory:"


def test_sqladatabase_is_async():
    db = SQLADatabase(url="sqlite:///:memory:")
    assert db.is_async() is False


def test_sqladatabase_session():
    db = SQLADatabase(url="sqlite:///:memory:")
    with pytest.raises(RuntimeError):
        db.session  # noqa


def test_sqladatabase_session_ctx():
    db = SQLADatabase(url="sqlite:///:memory:")
    with db.session_ctx() as session:
        assert session is not None
        assert db.session is not None
