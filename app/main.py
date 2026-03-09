from fastapi import FastAPI, Security

from app.api.v1 import chat
from app.core.config import settings
from app.core.security import verify_internal_token

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",  # Swagger UI 地址
    redoc_url="/redoc",  # Redoc 地址
    openapi_url=f"{settings.API_PREFIX}/openapi.json"  # OpenAPI 描述文件地址
)

app.include_router(
    chat.router,
    prefix=f"{settings.API_PREFIX}/chat",
    tags=["Chat Base"],
    dependencies=[Security(verify_internal_token)]
)


@app.get(path="/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "project": settings.APP_NAME,
        "env": settings.ENVIRONMENT
    }
