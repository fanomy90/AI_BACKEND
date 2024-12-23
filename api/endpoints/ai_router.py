import os

from fastapi import APIRouter, BackgroundTasks
from dotenv import load_dotenv

from crud.request import CRUDRequest
from services.constants import OK_MSG
from services.instruments import send_to_module

from schemas.ai_interact import Got_From_AI, API_Response
from schemas.bot_interact import FinalOutput

load_dotenv()
router = APIRouter()


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
    background_tasks.add_task(send_to_module(req_data, Got_From_AI,
                                             os.getenv('BOT_MODULE_LINK')))

    return API_Response(
        message_status=OK_MSG
    )
