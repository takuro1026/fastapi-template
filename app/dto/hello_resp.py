from pydantic import BaseModel


class HelloResp(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            'example': {
                'message': 'Takuro: Hello world!'
            }
        }
