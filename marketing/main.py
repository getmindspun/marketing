""" Main entry point """
import logging

import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import settings, middleware


logger = logging.getLogger(__name__)


async def validation_exception_handler(
        _request: fastapi.Request,
        exc: RequestValidationError
) -> JSONResponse:
    """ Logging validation exception handler """
    detail = exc.errors()
    logger.warning("422: %s, errors=%s", exc.body, detail)
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": detail, "body": exc.body}),
    )


def make_app() -> fastapi.FastAPI:
    """ Create the fastapi application """
    log_level = getattr(logging, str(settings.LOG_LEVEL).upper())
    logging.basicConfig(level=log_level)

    application = fastapi.FastAPI(
        title="Mindspun Marketing API",
        version=settings.VERSION,
        root_path=settings.ROOT_PATH
    )
    application.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    application.add_middleware(
        middleware.SessionMiddleware, bind=str(settings.DATABASE_URL)
    )
    return application


app = make_app()
