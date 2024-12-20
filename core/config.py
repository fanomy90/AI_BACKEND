from typing import Optional

from pydantic import BaseSettings  # , EmailStr


class Settings(BaseSettings):
    app_title: str = 'Fast4pics'
    database_url: str
    secret: str
    # first_superuser_email: Optional[EmailStr] = None
    # first_superuser_password: Optional[str] = None
    description: str = 'Органзация связи между ботом и нейромодулем'
    version: float = 0.1

    class Config:
        env_file = '.env'


settings = Settings()
