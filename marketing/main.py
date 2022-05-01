""" Main entry point """
import logging
from logging.handlers import RotatingFileHandler

import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from . import settings, middleware


logger = logging.getLogger(__name__)


def setup_logging():
    """ Setup logging """
    formatter = logging.Formatter(settings.LOG_FORMAT, settings.LOG_DATEFMT)

    marketing = logging.getLogger("marketing")

    if settings.LOG_PATH:
        handler = RotatingFileHandler(
            settings.LOG_PATH,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT
        )
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    handler.setLevel(settings.LOG_LEVEL)
    marketing.addHandler(handler)


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
    setup_logging()

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
