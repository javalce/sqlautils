import pytest
from sqlalchemy import Engine, Integer
from sqlalchemy.orm import Mapped, clear_mappers, mapped_column, sessionmaker
from sqlautils.core import SQLADatabase
from sqlautils.model import BaseModel


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


def test_sqladatabase_get_engine():
    db = SQLADatabase(url="sqlite:///:memory:")
    engine = db.get_engine()
    assert isinstance(engine, Engine)


def test_sqladatabase_metadatas():
    db = SQLADatabase(url="sqlite:///:memory:")
    metadatas = db.metadatas
    assert isinstance(metadatas, dict)


def test_sqladatabase_session_factory():
    db = SQLADatabase(url="sqlite:///:memory:")
    session_factory = db.session_factory
    assert isinstance(session_factory, sessionmaker)


def test_sqladatabase_bind_keys():
    class TestModel(BaseModel):
        __bind_key__ = "test"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    db = SQLADatabase(url="sqlite:///:memory:", binds={"test": "sqlite:///:memory:"})
    assert db.binds == {"test": "sqlite:///:memory:"}
    assert db.get_engine("test") is not None

    with pytest.raises(ValueError):
        db.get_engine("invalid")

    clear_mappers()
