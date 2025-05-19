from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_USER: str
    RMQ_PASS: str

    @property
    def get_rmq_dsn(self):
        return (
            f"amqp://{self.RMQ_USER}:{self.RMQ_PASS}@{self.RMQ_HOST}:{self.RMQ_PORT}/"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
