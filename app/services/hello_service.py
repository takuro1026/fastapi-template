from fastapi import APIRouter

from app.dto.hello_req import HelloReq
from app.dto.hello_resp import HelloResp

router = APIRouter(
    tags=["Service"],
    prefix="/v1"
)

class HelloService:

    def hello(self, request_id, hello_req: HelloReq):
        if not hello_req.description:
            message = f'{request_id} : {hello_req.name} : Hello world'
        else:
            message = f'{request_id} : {hello_req.name} : {hello_req.description}'

        return HelloResp(message=message)
