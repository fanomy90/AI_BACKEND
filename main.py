from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import main_router as api_router  # Импорт вашего роутера

app = FastAPI(
    title="Ваше API",  # Название вашего приложения
    description="Описание API",  # Краткое описание
    version="1.0.0"  # Версия API
)

# Настройка CORS (опционально, если вы планируете внешние подключения)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или ограничьте список доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(api_router, prefix="/api", tags=["API"])  # Префикс и тег для роутера

