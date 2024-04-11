from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


# Reference:
# https://fastapi.tiangolo.com/tutorial/body-fields/
# https://docs.pydantic.dev/latest/concepts/validators/

@dataclass
class HelloReq(BaseModel):
    name: str
    description: str | None = Field(default=None, title='The description of request', max_length=10)

    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    # you can select multiple fields, or use '*' to select all fields
    @field_validator('name', 'description')
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            # info.field_name is the name of the field being validated
            is_alphanumeric = v.replace(' ', '').isalnum()
            assert is_alphanumeric, f'{info.field_name} must be alphanumeric'
        return v
