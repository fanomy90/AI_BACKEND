import uuid


def generate_req_id() -> int:
    """
    Генерация уникального идентификатора на основе UUID.
    Преобразуем UUID в 64-битное число.
    """
    return uuid.uuid4().int >> 64
