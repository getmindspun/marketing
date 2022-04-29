""" Generic middleware """
import typing

from sqlalchemy.engine import Connectable, Engine, create_engine

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .models.base import Session


def register(
        bind: typing.Union[str, Connectable],
        pool_pre_ping=True,
        **engine_kwargs
) -> Engine:
    """Register an engine or create a new one (non thread-safe)."""
    if isinstance(bind, str):
        engine = create_engine(
            bind, pool_pre_ping=pool_pre_ping, **engine_kwargs)
        bind = engine

    return bind


class SessionMiddleware(BaseHTTPMiddleware):
    """Add a `models.Session` instance to `request.state.session` """
    def __init__(
            self,
            app: ASGIApp,
            bind: typing.Union[str, Connectable],
            **engine_kwargs
    ):
        super().__init__(app)
        bind = register(bind, **engine_kwargs)
        Session.configure(bind=bind)

    async def dispatch(
            self,
            request: Request,
            call_next
    ) -> Response:
        added = False
        try:
            if not hasattr(request.state, "session"):
                request.state.session = Session()
                added = True
            response = await call_next(request)
        finally:
            if added:
                # Only close a session if we added it, useful for testing
                request.state.session.close()
        return response
