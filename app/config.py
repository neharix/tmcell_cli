from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USER_LOGIN: str | None = None
    USER_PASSWORD: str | None = None

    @property
    def service_url(self):
        return "https://hyzmat.tmcell.tm"

    class Config:
        env_file = ".env"


settings = Settings()
