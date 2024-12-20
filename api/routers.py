from fastapi import APIRouter
from api.endpoints.ai_router import router as ai_router
from api.endpoints.bot_router import router as bot_router


main_router = APIRouter()
main_router.include_router(bot_router, prefix="/bot", tags=["bot_API"])
main_router.include_router(ai_router, prefix="/ai", tags=["ai_API"])
