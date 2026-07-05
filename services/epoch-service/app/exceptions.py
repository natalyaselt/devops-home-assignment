import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_friendly_message(error_type: str) -> str:
    """
    Convert Pydantic/FastAPI validation errors into user-friendly messages.

    Args:
        error_type: Validation error type reported by Pydantic.

    Returns:
        A human-readable error message.
    """

    messages = {
        "missing": "The 'date' field is required.",
        "datetime_from_date_parsing": (
            "Invalid date format. Expected ISO-8601 format " "(YYYY-MM-DDTHH:MM:SSZ)."
        ),
        "datetime_parsing": (
            "Invalid date format. Expected ISO-8601 format " "(YYYY-MM-DDTHH:MM:SSZ)."
        ),
        "json_invalid": "Malformed JSON request.",
        "string_type": "The 'date' field must be a string.",
    }

    return messages.get(error_type, "Invalid request.")


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers for the application.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle request validation errors.

        This includes:
        - Missing required fields
        - Invalid date format
        - Malformed JSON
        - Invalid request body
        """

        logger.warning(
            "Validation failed for %s %s",
            request.method,
            request.url.path,
        )

        errors: list[dict[str, Any]] = []

        for error in exc.errors():
            # Remove "body" from the location path.
            field = ".".join(str(item) for item in error["loc"][1:])

            errors.append(
                {
                    "field": field,
                    "message": get_friendly_message(error["type"]),
                }
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Request validation failed.",
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected server errors.
        """

        logger.exception(
            "Unexpected error while processing %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error."},
        )
