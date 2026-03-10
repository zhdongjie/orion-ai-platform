# app/core/constants.py
from enum import IntEnum


class ResponseCode(IntEnum):
    """业务状态码枚举"""
    SUCCESS = 20000  # 回答正确 / 操作成功
    UNAUTHORIZED = 40100  # 未授权
    FORBIDDEN = 40300  # 无权限
    SYSTEM_ERROR = 50000  # 系统异常
