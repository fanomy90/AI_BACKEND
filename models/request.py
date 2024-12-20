from sqlalchemy import Column, Boolean, Integer

from core.db import PreBase


class Request(PreBase):
    user_id = Column(Integer, nullable=False)
    process_done = Column(Boolean, nullable=False, default=False)
