from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.dto.hello_req import HelloReq
from app.services.hello_service import HelloService
from app.utils.utils import time_fn, async_time_fn

router = APIRouter(
    tags=['Service'],
    prefix='/v1'
)

@router.post('/hello')
@async_time_fn
async def hello_post(
    req: HelloReq,
    service: HelloService = Depends(HelloService),
    x_request_id: Annotated[str | None, Header(include_in_schema=True)] = None
):
    return service.hello(x_request_id, req)
