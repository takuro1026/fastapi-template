from http import HTTPStatus

from fastapi import HTTPException

from app.exceptions.error_code import ErrorCode


class ServiceException(HTTPException):
    def __init__(self, status_code: HTTPStatus, error: str, message: str):
        self.status_code = status_code
        self.error = error
        self.detail = message

    @classmethod
    def from_error_code(cls, error_code: ErrorCode):
        return ServiceException(
            status_code=error_code.status_code,
            error=error_code.error,
            message=error_code.detail
        )
