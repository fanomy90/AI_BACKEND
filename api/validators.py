from http import HTTPStatus
from typing import NoReturn

import os
import requests

from dotenv import load_dotenv
from fastapi import HTTPException
import validators  # сторонняя либа

from services.constants import PIC_FILE, PIC_SIZE, ONE_MB_SIZE

load_dotenv()


async def confirm_request_token(token: str) -> NoReturn:
    """Убеждается что запрос пришел от бота,
    простым сравнением токена."""
    if not token or token != os.getenv('TOKEN'):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Кто-то тут не тот.',
        )


async def check_got_pic(
        link: str,
) -> NoReturn:
    """Проверяет хвост линка на соответствие расширеням картинок,
    на данный момент только jpg, jpeg, png, редактируйте services.constants."""
    tail = (os.path.splitext(link))[1]
    if tail.lower not in PIC_FILE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Расширение файла не соответствует графике.',
        )


async def check_link_valid_alive(
        link: str,
) -> NoReturn:
    """Линк валидный и отвечает статусом 200."""
    detail = 'Ваша ссылка не ссылка'
    if validators.url(link) is True:
        if (requests.head(link)).status_code == HTTPStatus.OK:
            return
        detail = 'Ваша ссылка не работает'
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=detail
    )


async def check_file_size(
        link: str
) -> NoReturn:
    """Проверка размера файла (без скачивания)"""
    info = (requests.head(link)).headers
    if not info:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Не удалось получить headers (информацию о файле)'
        )
    if info.get('Content-Length') > PIC_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Слишком большой файл, лимит {PIC_SIZE/ONE_MB_SIZE} Mб'
        )
