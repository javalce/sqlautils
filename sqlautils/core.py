from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator, Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

_session: ContextVar[Union[Session, None]] = ContextVar("_session", default=None)


class SQLADatabase:
    def __init__(
        self,
        url: Union[str, None] = None,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ):
        """Initialize the database connection.

        :param url: The database URL.
        :param engine_options: The engine options.
        :param session_options: The session options.

        This method initializes the instance with the given parameters. The actual
        initialization of the database connection is performed by calling the
        `initialize` method.
        """
        self.engine_options = engine_options or {}
        self.session_options = session_options or {}

        self.url: Union[str, None] = None
        self.engine: Union[Engine, None] = None

        if url:
            self.initialize(url)

    def initialize(
        self,
        url: Union[str, None] = None,
        engine_options: Union[Dict[str, Any], None] = None,
        session_options: Union[Dict[str, Any], None] = None,
    ) -> None:
        """Initialize the database connection.

        :param url: The database URL.
        :param engine_options: The engine options.
        :param session_options: The session options.

        This method must be called explicitly to complete the initialization of
        the instance the two-phase initialization method is used.
        """
        if url is None:
            raise ValueError('"url" must be set')

        self.url = url
        self.engine_options = engine_options or self.engine_options
        self.session_options = session_options or self.session_options

        options = self.engine_options
        options.setdefault("future", True)
        self.engine = create_engine(self.url, **options)
        self.session_factory = sessionmaker(bind=self.engine, **self.session_options)

    def is_async(self) -> bool:
        """Returns whether the database is an async database or not.

        This method should be overridden by subclasses to return the correct value."""
        return False

    @property
    def session(self) -> Session:
        """Return a new session."""
        session = _session.get()

        if session is None:
            raise RuntimeError("No session is available")

        return session

    @contextmanager
    def session_ctx(self) -> Iterator[Session]:
        """Return a context manager that provides a session.

        This method returns a context manager that provides a session. The session
        is removed from the context when the context manager exits. If a session is
        already present in the context, it is used instead of creating a new one.

        Example:
        with db.session_ctx() as session:
            session.query(...)
        """
        session = _session.get()

        if session is None:
            session = self.session_factory()
            _session.set(session)

        try:
            yield session
        finally:
            session.close()
            _session.set(None)
