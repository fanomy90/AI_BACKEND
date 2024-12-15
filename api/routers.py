from fastapi import APIRouter

from api.endpoints import (
    bot_router, ai_router
)

main_router = APIRouter()
main_router.include_router(
    bot_router, prefix='/bot_router', tags=['bot_router']
)
main_router.include_router(
    ai_router, prefix='/ai_router', tags=['ai_router']
)
