import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("deepshield.api")


async def validation_error_handler(_: Request, exception: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"error": "validation_error", "details": exception.errors()})


async def database_error_handler(_: Request, exception: SQLAlchemyError) -> JSONResponse:
    logger.error("Database operation failed", exc_info=(type(exception), exception, exception.__traceback__))
    return JSONResponse(status_code=503, content={"error": "database_unavailable", "message": "The data service is temporarily unavailable."})


async def unexpected_error_handler(_: Request, exception: Exception) -> JSONResponse:
    logger.error("Unhandled API error", exc_info=(type(exception), exception, exception.__traceback__))
    return JSONResponse(status_code=500, content={"error": "internal_error", "message": "The request could not be completed."})
