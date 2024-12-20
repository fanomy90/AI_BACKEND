from typing import Optional

from pydantic import BaseModel, Field


class Send_To_AI(BaseModel):
    req_id: int = Field(...,)
    link: str = Field(...,)


class Got_From_AI(BaseModel):
    req_id: int = Field(...,)
    message: str = Field(...,)
    error: Optional[str] = Field(None,)


class API_Response(BaseModel):
    msg_status: str = Field(...,)
