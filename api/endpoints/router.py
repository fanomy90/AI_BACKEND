from fastapi import APIRouter, HTTPException, BackgroundTasks
import httpx
from http import HTTPStatus
import os

from dotenv import load_dotenv
from api.validators import (
    check_file_size, check_got_pic, check_link_valid_alive,
    confirm_request_token
)
from services.constants import (
    OK_MSG
)
from services.make_req_id import generate_req_id
from schemas.bot_interact import InitInput, InitOutput
from schemas.ai_interact import Send_to_ai, Got_from_ai

router = APIRouter()


async def send_to_next_module(req_data: Send_to_ai):
    """
    Асинхронная функция для отправки данных в следующий модуль.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                os.getenv('STORAGE_MODULE_LINK'),
                json=req_data.dict()
            )
            if response.status_code == HTTPStatus.OK:
                # Валидация и обработка ответа
                return Got_from_ai(**response.json())
            else:
                # Обработка ошибок от следующего модуля
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ошибка от следующего модуля: {response.text}"
                )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=HTTPStatus.BAD_GATEWAY,
                detail=f"Ошибка подключения к модулю хранения: {exc}"
            )


@router.post(
    '/',
    response_model=InitOutput
)
async def create_new_iteration(
    input: InitInput,
    background_tasks: BackgroundTasks,
):
    """
    Обрабатывает первичный запрос, возвращает сообщение о начале обработки,
    а затем выполняет запрос к следующему модулю.
    """
    # Проверка входных данных
    await confirm_request_token(input.token)
    await check_link_valid_alive(input.link)
    await check_got_pic(input.link)
    await check_file_size(input.link)

    # Генерация уникального идентификатора запроса
    req_id = await generate_req_id()

    # Формирование данных для следующего модуля
    req_data = Send_to_ai(req_id=req_id, link=input.link)

    # Добавление задачи в фоновый процесс
    background_tasks.add_task(send_to_next_module, req_data)

    # Возвращаем сообщение об успешной обработке первичного запроса
    return InitOutput(
        message=OK_MSG,
        status_code=HTTPStatus.ACCEPTED
    )
