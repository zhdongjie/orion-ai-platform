# app/core/exceptions.py
from typing import Optional, Union

from app.core.constants import ResponseCode


class AppException(Exception):
    """
    Orion 平台基础异常类
    所有业务自定义异常都应继承此类
    """
    msg: str
    code: int
    data: Optional[dict]

    def __init__(
            self,
            msg: str,
            code: Union[ResponseCode, int] = ResponseCode.SYSTEM_ERROR,
            data: Optional[dict] = None
    ):
        self.msg = msg
        self.code = code.value
        self.data = data
        super().__init__(msg)


class BusinessException(AppException):
    """
    通用业务逻辑异常
    例如：信用卡额度校验失败、参数非法等
    默认状态码: ANSWER_ERROR (40000)
    """

    def __init__(self, msg: str, code: ResponseCode = ResponseCode.ANSWER_ERROR):
        super().__init__(msg, code=code)


class LLMProviderException(AppException):
    """
    大模型提供商调用异常
    例如：API Key 过期、模型欠费、请求超时、模型不存在等
    默认状态码: ANSWER_ERROR (40000)
    """

    def __init__(self, msg: str):
        super().__init__(msg, code=ResponseCode.ANSWER_ERROR)


class PromptException(AppException):
    """
    提示词配置异常
    例如：YAML 提示词文件不存在、格式解析错误、变量缺失等
    默认状态码: SYSTEM_ERROR (50000)
    """

    def __init__(self, msg: str):
        super().__init__(msg, code=ResponseCode.SYSTEM_ERROR)


class AuthException(AppException):
    """
    认证与授权异常
    例如：Token 失效、无权访问特定模型或模块
    """

    def __init__(self, msg: str, is_forbidden: bool = False):
        code = ResponseCode.FORBIDDEN if is_forbidden else ResponseCode.UNAUTHORIZED
        super().__init__(msg, code=code)


class DatabaseException(AppException):
    """
    数据库操作异常
    用于 Phase 2 向量数据库或关系型数据库连接失败、查询报错
    """

    def __init__(self, msg: str):
        super().__init__(msg, code=ResponseCode.SYSTEM_ERROR)
