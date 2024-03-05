from contextlib import contextmanager
from threading import Lock
from typing import Any, Dict, Iterator, Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .model import BaseModel
from .session import _session, get_session


class SQLADatabase:
    def __init__(
        self,
        url: Union[str, None] = None,
        binds: Union[Dict[str, Any], None] = None,
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

        self.lock = Lock()
        self.url: Union[str, None] = None
        self.binds: Union[Dict[str, Any], None] = None
        self.engines: Dict[Union[str, None], Engine] = {}
        self.table_binds: Dict[str, Engine] = {}

        if url or binds:
            self.initialize(url, binds=binds)

    def initialize(
        self,
        url: Union[str, None] = None,
        binds: Union[Dict[str, Any], None] = None,
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
        if url is None and binds is None:
            raise ValueError('"url" and/or "binds" must be set')

        self.url = url
        self.binds = binds
        self.engine_options = engine_options or self.engine_options
        self.session_options = session_options or self.session_options

        options = self.engine_options
        options.setdefault("future", True)

        self._create_engines()
        self._create_session_factory()

    def _create_engines(self) -> None:
        """Create the engines."""

        options = self.engine_options
        options.setdefault("future", True)

        if self.url:
            self.engines[None] = create_engine(self.url, **options)

        for bind_key, url in (self.binds or {}).items():
            self.engines[bind_key] = create_engine(url, **options)

            for table in BaseModel.__metadatas__[bind_key].tables.values():
                self.table_binds[table] = self.engines[bind_key]

    def _create_session_factory(self) -> None:
        """Create the session factory."""

        self.session_factory = sessionmaker(
            bind=self.get_engine(),
            binds=self.table_binds,
            **self.session_options,
        )

    def get_engine(self, bind: Union[str, None] = None) -> Engine:
        """Return the engine for the given bind.

        :param bind: The bind name.

        This method returns the engine for the given bind. If no bind is given, the
        default engine is returned.
        """
        engine = self.engines.get(bind)

        if engine is None:
            raise ValueError(f'No engine found for bind "{bind}"')

        return engine

    @property
    def metadatas(self) -> Dict[str, Any]:
        return BaseModel.__metadatas__

    def is_async(self) -> bool:
        """Returns whether the database is an async database or not.

        This method should be overridden by subclasses to return the correct value."""
        return False

    @property
    def session(self) -> Session:
        """Return a new session."""
        return get_session()

    @contextmanager
    def session_ctx(self) -> Iterator[Session]:
        """Return a context manager that provides a session.

        This method returns a context manager that provides a session. The session
        is removed from the context when the context manager exits. If a session is
        already present in the context, it is used instead of creating a new one.

        Example:
        with db.session_ctx() as session:
            session.execute(...)
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
