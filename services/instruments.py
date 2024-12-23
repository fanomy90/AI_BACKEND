import uuid
import httpx
from http import HTTPStatus

from fastapi import HTTPException


def generate_req_id() -> int:
    """
    Генерация уникального идентификатора на основе UUID.
    Преобразуем UUID в 64-битное число.
    """
    return uuid.uuid4().int >> 64


async def send_to_module(req_data, schema, module_url: str):
    """
    Универсальная асинхронная функция для отправки данных в указанный модуль.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                module_url,
                json=req_data.dict()
            )
            if response.status_code == HTTPStatus.OK:
                # Валидация и обработка ответа
                return schema(**response.json())
            else:
                # Обработка ошибок от модуля
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ошибка от модуля ({module_url}): {response.text}"
                )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=HTTPStatus.BAD_GATEWAY,
                detail=f"Ошибка подключения к модулю ({module_url}): {exc}"
            )
