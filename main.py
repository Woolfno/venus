import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from admin.models import Admin
from admin.providers import LoginProvider
from starlette.middleware.cors import CORSMiddleware
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise

from routes import router
from settings import settings


admin_app.add_exception_handler(
    HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
admin_app.add_exception_handler(
    HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

app = FastAPI(title="Tortoise ORM FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.mount('/admin', admin_app)
app.include_router(router)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["models", 'admin.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event('startup')
async def startup():
    await admin_app.configure(
        template_folders=[settings.ADMIN_TEMPLATES_DIR],
        providers=[
            LoginProvider(
                login_logo_url="/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding='utf-8'),

    )

import logging
import sys

fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.DEBUG)
logger_tortoise.addHandler(sh)