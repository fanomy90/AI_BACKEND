from fastapi import APIRouter, BackgroundTasks, HTTPException
import httpx
from http import HTTPStatus

from api.validators import (
    check_file_size, check_got_pic, check_link_valid_alive
)
from services.constants import (
    STORAGE_MODULE_LINK, OK_MSG, NOT_OK_MSG
)
from schemas.bot_interact import (
    InitInput, InitOutput,
)

router = APIRouter()

def process_request(input: InitInput):
    """Фоновая задача для обработки запроса."""
    async def background_processing():
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(STORAGE_MODULE_LINK, json={"link": input.link})
                if response.status_code == HTTPStatus.OK:
                    processing_result = response.json().get("success")
                    # Логика обработки ответа от модуля
                    if processing_result:
                        print("Processing completed successfully")
                    else:
                        print("Processing failed")
                else:
                    print(f"Error from processing module: {response.text}")
            except httpx.RequestError as exc:
                print(f"HTTP request error: {exc}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    import asyncio
    asyncio.run(background_processing())

@router.post(
    '/',
    response_model=InitOutput
)
async def create_new_iteration(
    input: InitInput, background_tasks: BackgroundTasks
):
    """Эндпоинт запуска обработки с немедленным ответом."""
    # Проверяем входные данные
    await check_link_valid_alive(input.link)
    await check_got_pic(input.link)
    await check_file_size(input.link)
    
    # Добавляем обработку в фоновую задачу
    background_tasks.add_task(process_request, input)
    
    # Немедленный ответ клиенту
    return InitOutput(
        message=OK_MSG,
        status_code=HTTPStatus.ACCEPTED
    )
