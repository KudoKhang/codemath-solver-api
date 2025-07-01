from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    status_code: int
    data: Optional[Any] = None
    message: Optional[str] = None

    @classmethod
    def success(cls, data: Any = None, status_code: int = 200, message: Optional[str] = "Success"):
        return cls(status_code=status_code, data=data, message=message)

    @classmethod
    def failure(cls, message: str, status_code: int = 400, data: Any = None):
        return cls(status_code=status_code, data=data, message=message)
