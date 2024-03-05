import pytest
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, clear_mappers, mapped_column
from sqlautils.model import BaseModel


@pytest.fixture(autouse=True)
def teardown_function():
    yield
    BaseModel.metadata.clear()
    clear_mappers()


def test_base_model_default_tablename():
    class DummyModel(BaseModel):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(DummyModel, DeclarativeBase)
    assert getattr(DummyModel, "__tablename__", None) == "dummy_model"


def test_base_model_tablename_custom():
    class DummyModel(BaseModel):
        __tablename__ = "dummy_table"

        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    assert issubclass(DummyModel, DeclarativeBase)
    assert getattr(DummyModel, "__tablename__", None) == "dummy_table"
