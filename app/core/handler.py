# app/core/handler.py
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.core.constants import ResponseCode
from app.core.exceptions import AppException
from app.schemas import Result


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        """捕获业务异常，返回 200 状态码，内容中包含 5 位数代码"""
        return JSONResponse(
            status_code=200,
            content=Result.fail(code=exc.code, msg=exc.msg).__dict__
        )

    @app.exception_handler(Exception)
    async def app_exception_handler(_: Request, __: Exception):
        """捕获系统崩溃，返回 50000 系统异常"""
        return JSONResponse(
            status_code=500,
            content=Result.fail(
                code=ResponseCode.SYSTEM_ERROR.value,
                msg="服务器开小差了"
            ).__dict__
        )
