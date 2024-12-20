import httpx
from http import HTTPStatus
import os

from fastapi import APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv

from crud.request import CRUDRequest
from services.constants import (
    OK_MSG
)
from schemas.ai_interact import Send_To_AI, Got_From_AI, API_Response
from schemas.bot_interact import FinalOutput

load_dotenv()
router = APIRouter()


async def send_to_bot_module(req_data: Send_To_AI):
    """
    Асинхронная функция для отправки данных в следующий модуль.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                os.getenv('BOT_MODULE_LINK'),
                json=req_data.dict()
            )
            if response.status_code == HTTPStatus.OK:
                # Валидация и обработка ответа
                return Got_From_AI(**response.json())
            else:
                # Обработка ошибок от следующего модуля
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ошибка от следующего модуля: {response.text}"
                )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=HTTPStatus.BAD_GATEWAY,
                detail=f"Ошибка подключения к модулю бота: {exc}"
            )


@router.post(
    '/',
    response_model=API_Response,
)
async def got_response_from_ai(
    input: Got_From_AI,
    background_tasks: BackgroundTasks,
):
    """
    Обрабатывает ответ от ai-модуля.
    """
    user_id = await CRUDRequest.get_user_id_by_req_id(input.req_id)

    # Формирование данных для следующего модуля
    req_data = FinalOutput(user_id=user_id, message=input.message)

    # Добавление задачи в фоновый процесс
    background_tasks.add_task(send_to_bot_module, req_data)

    return API_Response(
        message_status=OK_MSG
    )
