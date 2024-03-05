from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from ...core import SQLADatabase


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, db: SQLADatabase) -> None:
        """Initialize the middleware.

        :param app: The ASGI application.
        :param database: The database instance.

        This method initializes the middleware with the given parameters.
        """
        super().__init__(app)
        self.db = db

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch the request.

        :param request: The request.
        :param call_next: The next request handler.

        This method dispatches the request by setting up the database session and
        calling the next request handler.
        """
        with self.db.session_ctx():
            response = await call_next(request)

        return response
