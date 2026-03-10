from contextlib import asynccontextmanager

from fastapi import FastAPI, Security
from loguru import logger

from app.api.v1 import chat
from app.core.config import settings
from app.core.handler import register_exception_handlers
from app.core.logger import setup_logging
from app.core.security import verify_internal_token


@asynccontextmanager
async def lifespan(_):
    # 启动前执行：初始化日志
    setup_logging()
    logger.info("系统正在启动...")

    yield
    # 停止前执行：可以在这里关闭数据库连接池等
    logger.info("系统正在优雅关闭...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
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

register_exception_handlers(app)


@app.get(path="/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "project": settings.APP_NAME,
        "env": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",  # 注意这里必须是字符串形式
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.ENVIRONMENT == "dev",  # 如果是开发环境则开启热更新
    )
