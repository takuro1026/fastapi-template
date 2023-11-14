from app.dto.hello_req import HelloReq
from app.dto.hello_resp import HelloResp


class HelloService:

    def hello(self, hello_req: HelloReq):
        if not hello_req.description:
            message = f'{hello_req.name}: Hello world'
        else:
            message = f'{hello_req.name}: {hello_req.description}'

        return HelloResp(message=message)
