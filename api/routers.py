from fastapi import APIRouter
from api.endpoints.router import router  # Импорт ваших эндпоинтов

main_router = APIRouter()
main_router.include_router(router, prefix="/router", tags=["router"])
