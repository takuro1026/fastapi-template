import sys
from http import HTTPStatus

from typing import Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import request_validation_exception_handler, http_exception_handler
from starlette.responses import JSONResponse, Response, PlainTextResponse

from app.exceptions.service_exception import ServiceException
from app.utils.logger import logger

# Reference: https://fastapi.tiangolo.com/tutorial/handling-errors/
class ExceptionHandler:

    @classmethod
    async def validation_exception_handler(cls, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        This is a wrapper to the default RequestValidationException handler of FastAPI.
        This function will be called when client input is not valid.
        """
        return await request_validation_exception_handler(request, exc)

    @classmethod
    async def http_request_exception_handler(cls, request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
        """
        This is a wrapper to the default HTTPException handler of FastAPI.
        This function will be called when a HTTPException is explicitly raised.
        """
        return await http_exception_handler(request, exc)

    @classmethod
    async def service_exception_handler(cls, request: Request, exc: ServiceException) -> Union[JSONResponse, Response]:
        """
        This is the exception handler for this service which handling service exception class.
        This function will be called when a ServiceException is explicitly raised.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=vars(exc)
        )

    @classmethod
    async def unhandled_exception_handler(cls, request: Request, exc: Exception) -> JSONResponse:
        """
        This middleware will log all unhandled exceptions.
        Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
        """
        host = getattr(getattr(request, 'client', None), 'host', None)
        port = getattr(getattr(request, 'client', None), 'port', None)
        url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
        exception_type, exception_value, exception_traceback = sys.exc_info()
        exception_name = getattr(exception_type, '__name__', None)
        logger.error(
            f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
        )
        return JSONResponse(
            content={'detail': str(exc)},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )
