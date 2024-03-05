# FILEPATH: /home/javalce/Dev/sqlautils/tests/test_model.py

import pytest
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, clear_mappers, mapped_column
from sqlautils.model import BaseModel


@pytest.fixture(autouse=True)
def teardown_function():
    yield
    BaseModel.metadata.clear()
    clear_mappers()


@pytest.fixture
def DummyModel():
    class DummyModel(BaseModel):
        id: Mapped[int] = mapped_column(Integer, primary_key=True)

    return DummyModel


def test_base_model_tablename(DummyModel):
    assert DummyModel.__tablename__ == "dummymodel"


def test_base_model_name(DummyModel):
    assert DummyModel.__name__ == "DummyModel"
