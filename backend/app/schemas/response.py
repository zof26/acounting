from pydantic import BaseModel
from typing import Any

class ErrorResponse(BaseModel):
    detail: Any
