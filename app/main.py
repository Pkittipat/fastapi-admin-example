import os
import aioredis
from fastapi_admin.app import app as admin_app
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app import settings
from starlette.staticfiles import StaticFiles
from app.constants import BASE_DIR
from starlette.responses import RedirectResponse
from app.providers import LoginProvider
from app.models import Admin
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
)

app = FastAPI()
app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

@app.get("/")
async def index():
    return RedirectResponse(url="/admin")

@app.get("/something")
async def test():
    return


admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(settings.REDIS_URL, encoding="utf8")
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=redis,
    )

app.mount("/admin", admin_app)
register_tortoise(
    app,
    config={
        "connections": {"default": settings.DATABASE_URL},
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "default",
            }
        },
    },
    generate_schemas=True,
)
