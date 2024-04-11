from enum import Enum
from http import HTTPStatus


class ErrorCode(Enum):
    BAD_REQUEST = HTTPStatus.BAD_REQUEST, 'BAD_REQUEST', 'the request is invalid'

    def __init__(self, status_code: HTTPStatus, error: str, detail: str):
        self.status_code = status_code
        self.error = error
        self.detail = detail