from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/darkroom"
    APP_NAME: str = "Darkroom API"
    DEBUG: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["service.models.item", "aerich.models"],
            "default_connection": "default",
        }
    },
}
