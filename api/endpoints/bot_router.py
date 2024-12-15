from fastapi import APIRouter, HTTPException
import httpx
from http import HTTPStatus

from api.validators import (
    check_file_size, check_got_pic, check_link_valid_alive)
from services.constants import (
    STORAGE_MODULE_LINK, OK_MSG, NOT_OK_MSG)
from schemas.bot_interact import (
    InitInput, InitOutput,)


router = APIRouter()


@router.post(
    '/',
    response_model=InitOutput
)
async def create_new_iteration(
        input: InitInput,
):
    await check_link_valid_alive(input.link)
    await check_got_pic(input.link)
    await check_file_size(input.link)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(STORAGE_MODULE_LINK, json={"link": input.link})
            
            # Обработка успешного ответа
            if response.status_code == HTTPStatus.OK:
                return InitOutput(
                    message=OK_MSG,
                    status_code=HTTPStatus.OK
                )
            else:
                # Обработка ошибки от модуля хранения
                return InitOutput(
                    message=NOT_OK_MSG,
                    error=response.text,
                    status_code=response.status_code
                )
        except httpx.RequestError as exc:
            # Обработка ошибок связи с модулем
            raise HTTPException(
                status_code=HTTPStatus.BAD_GATEWAY,
                detail=f"Ошибка подключения к модулю хранения: {exc}"
            )
        except Exception as error:
            # Общая обработка исключений
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Неизвестная ошибка: {error}"
            )