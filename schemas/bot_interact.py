from typing import Optional

from pydantic import BaseModel, Field


from services.constants import LINK_LEN_MIN, LINK_LEN_MAX, ID_LEN_MIN, ID_LEN_MAX


class InitInput(BaseModel):
    token: Optional[str] = Field(None,)
    user_id: int = Field(..., ge=ID_LEN_MIN, le=ID_LEN_MAX)
    link: str = Field(..., min_length=LINK_LEN_MIN, max_length=LINK_LEN_MAX)


class InitOutput(BaseModel):
    message: str = Field(...,)
    error: Optional[str] = Field(None,)
    status_code: Optional[int] = Field(None,)


