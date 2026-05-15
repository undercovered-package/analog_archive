from contextlib import asynccontextmanager

from service.config import settings, TORTOISE_ORM
from service.api.routers import health, items
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from service.core.errors.exception_handlers import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.0.1",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )


    origins = (
        []
        if settings.ENVIRONMENT == "production"
        else ["*"]
    )

    # origin_regexes = ()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origin_regex=origin_regexes,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(app)

    app.include_router(health.router, tags=["health"])
    app.include_router(items.router, prefix="/api/v1", tags=["items"])

    return app
