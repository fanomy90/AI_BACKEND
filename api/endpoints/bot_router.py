from fastapi import APIRouter, BackgroundTasks
from http import HTTPStatus
import os

from dotenv import load_dotenv
from api.validators import (
    check_file_size, check_got_pic, check_link_valid_alive,
    confirm_request_token
)
from services.constants import OK_MSG
from services.instruments import send_to_module
from services.instruments import generate_req_id
from schemas.bot_interact import InitInput, InitOutput
from schemas.ai_interact import Send_To_AI, Got_From_AI

load_dotenv()
router = APIRouter()


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
    req_data = Send_To_AI(req_id=req_id, link=input.link)

    # Добавление задачи в фоновый процесс
    background_tasks.add_task(send_to_module(req_data, Got_From_AI,
                                             os.getenv('STORAGE_MODULE_LINK')))

    # Возвращаем сообщение об успешной обработке первичного запроса
    return InitOutput(
        message=OK_MSG,
        status_code=HTTPStatus.ACCEPTED
    )
