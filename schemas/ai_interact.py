from typing import Optional

from pydantic import BaseModel, Field


class Send_to_ai(BaseModel):
    req_id: int = Field(...,)
    link: str = Field(...,)


class Got_from_ai(BaseModel):
    req_id: int = Field(...,)
    message: str = Field(...,)
    error: Optional[str] = Field(None,)
