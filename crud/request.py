from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.request import Request


class CRUDRequest(CRUDBase):

    async def get_user_id_by_req_id(
            self,
            req_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_user_id = await session.execute(
            select(Request.user_id).where(
                Request.id == req_id
            )
        )
        return db_user_id.scalars().first()


project_crud = CRUDRequest(Request)
