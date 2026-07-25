from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from src.apps.core.response import APIResponse
from src.core.logger import get_logger

logger = get_logger(__name__)


class AppException(HTTPException):
    """Base application exception with error code."""

    def __init__(
        self,
        status_code: int,
        error_code: int,
        message: str = "服务器内部错误",
        data: Any = None,
    ):
        self.error_code = error_code
        self.data = data
        super().__init__(status_code=status_code, detail=message)


class NotFound(AppException):
    """Resource not found (30001)."""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(status_code=404, error_code=30001, message=message)


class Unauthorized(AppException):
    """Not authenticated (10001)."""

    def __init__(self, message: str = "未登录"):
        super().__init__(status_code=401, error_code=10001, message=message)


class TokenExpired(AppException):
    """Token expired (10002)."""

    def __init__(self, message: str = "Token 已过期"):
        super().__init__(status_code=401, error_code=10002, message=message)


class Forbidden(AppException):
    """No permission (10003)."""

    def __init__(self, message: str = "无权限"):
        super().__init__(status_code=403, error_code=10003, message=message)


class BadRequest(AppException):
    """Bad request (20001)."""

    def __init__(self, message: str = "参数错误"):
        super().__init__(status_code=400, error_code=20001, message=message)


class DuplicateOperation(AppException):
    """Duplicate operation (30002)."""

    def __init__(self, message: str = "重复操作"):
        super().__init__(status_code=409, error_code=30002, message=message)


class NotImplemented(AppException):
    """Feature not implemented (50100)."""

    def __init__(self, message: str = "功能开发中"):
        super().__init__(status_code=501, error_code=50100, message=message)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException and return unified response format."""
    error_code = 50000
    if isinstance(exc, AppException):
        error_code = exc.error_code

    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            code=error_code,
            message=exc.detail,
            data=None,
        ).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions with a 500 response."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            code=50000,
            message="服务器内部错误",
            data=None,
        ).model_dump(),
    )
