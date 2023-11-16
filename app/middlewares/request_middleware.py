import http
import json
import time
import uuid
from json import JSONDecodeError

from typing import Tuple, Dict, List, Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response
from starlette.types import Message

from app.utils.logger import logger


# https://www.starlette.io/middleware/#basehttpmiddleware
class RequestMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    # https://github.com/tiangolo/fastapi/discussions/8187
    @classmethod
    async def set_body(cls, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    # https://github.com/encode/starlette/issues/495
    @classmethod
    async def _get_response_params(cls, response: StreamingResponse) -> Tuple[bytes, Dict[str, str], int]:
        """Getting the response parameters of a response and create a new response."""
        response_byte_chunks: List[bytes] = []
        response_status: List[int] = []
        response_headers: List[Dict[str, str]] = []

        async def send(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_status.append(message["status"])
                response_headers.append({k.decode("utf8"): v.decode("utf8") for k, v in message["headers"]})
            else:
                response_byte_chunks.append(message["body"])

        await response.stream_response(send)

        content = b"".join(response_byte_chunks)

        return content, response_headers[0], response_status[0]

    async def request_and_response_log_process(
            self,
            request,
            call_next: Callable[[Request], Awaitable[StreamingResponse]]
    ):
        """
        This middleware will log all requests and their processing time.
        E.g. log:
        0.0.0.0:1234 - GET /ping 200 OK 1.00ms
        """
        url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path

        headers = dict(request.scope['headers'])

        request_id = headers.get(b"x-request-id")

        if not request_id:
            request_id = str(uuid.uuid4())
            headers[b"x-request-id"] = bytes(request_id, "utf-8")
        else:
            request_id = str(request_id, 'UTF-8')

        request.scope['headers'] = [(k, v) for k, v in headers.items()]

        await self.set_body(request)

        request_body = await request.body()

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        formatted_process_time = "{0:.2f}".format(process_time)

        response.headers["x-process-time"] = formatted_process_time
        response.headers["x-request-id"] = request_id

        host = getattr(getattr(request, "client", None), "host", None)
        port = getattr(getattr(request, "client", None), "port", None)

        response_content_bytes, response_headers, response_status = await self._get_response_params(response)

        # If there is no request body handle exception; otherwise convert bytes to JSON.
        try:
            request_body = json.loads(request_body)
        except JSONDecodeError:
            request_body = ""

        try:
            response_body = json.loads(response_content_bytes)
        except JSONDecodeError:
            response_body = ""

        try:
            status_phrase = http.HTTPStatus(response.status_code).phrase
        except ValueError:
            status_phrase = ""

        info = json.dumps({
            "request_body": request_body,
            "response_body": response_body
        })

        logger.info(
            f'{host}:{port} - "{request.method} {url}" '
            f'request_id: {request_id} - '
            f'{response.status_code} {status_phrase} {formatted_process_time}s '
            f'{info}'
        )

        return Response(response_content_bytes, response_status, response_headers)

    async def dispatch(self, request, call_next: Callable[[Request], Awaitable[StreamingResponse]]):
        if request.url.path.startswith("/api"):
            return await self.request_and_response_log_process(request, call_next)
        else:
            response = await call_next(request)
            return response
