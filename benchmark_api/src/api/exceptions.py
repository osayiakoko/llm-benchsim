from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .response import APIResponse


def setup_exceptions(app: FastAPI) -> FastAPI:
    """
    Configures exception handlers for a FastAPI application.

    Args:
        app (FastAPI): The FastAPI application to configure.

    Returns:
        FastAPI: The configured FastAPI application.

    Sets up exception handlers for StarletteHTTPException, RequestValidationError,
    and general Exception. These handlers return APIResponse objects with
    appropriate error messages and status codes.
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Handles HTTP exceptions by returning an APIResponse with the exception details and status code.

        Parameters:
            request (Request): The incoming request that triggered the exception.
            exc (StarletteHTTPException): The Starlette HTTP exception that was raised.

        Returns:
            APIResponse: An API response containing the exception details and status code.
        """
        return APIResponse(str(exc.detail), status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Exception handler for RequestValidationError.

        Args:
            request (Request): The incoming request.
            exc (RequestValidationError): The validation exception.

        Returns:
            APIResponse: The API response with the validation error message and status code.
        """
        return APIResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        Handles general exceptions by returning an APIResponse with a generic error message and a 500 status code.

        Parameters:
            request (Request): The incoming request that triggered the exception.
            exc (Exception): The exception that was raised.

        Returns:
            APIResponse: An API response containing a generic error message and a 500 status code.
        """
        return APIResponse(
            "Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
