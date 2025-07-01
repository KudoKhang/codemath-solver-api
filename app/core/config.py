import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("POSTGRES_SERVER")
    DB_PORT: str = os.getenv("POSTGRES_PORT")
    DB_NAME: str = os.getenv("POSTGRES_DB")


settings = Settings()
