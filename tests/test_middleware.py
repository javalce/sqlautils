import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlautils.core import SQLADatabase
from sqlautils.ext.fastapi.middleware import SQLAlchemyMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


@pytest.fixture
def db():
    return SQLADatabase("sqlite:///:memory:")


def test_sqlalchemy_middleware_init(db):
    app = FastAPI()
    middleware = SQLAlchemyMiddleware(app, db)
    assert isinstance(middleware, BaseHTTPMiddleware)
    assert middleware.app == app
    assert middleware.db == db


def test_sqlalchemy_middleware(db):
    app = FastAPI()
    app.add_middleware(SQLAlchemyMiddleware, db=db)

    @app.get("/")
    def root():
        assert db.session is not None

    with TestClient(app) as client:
        client.get("/")
