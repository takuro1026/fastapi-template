from dataclasses import dataclass
from typing import List

from pydantic import BaseModel


@dataclass
class TestReq(BaseModel):
    images: List[str]


class TestResp(BaseModel):
    message: str
