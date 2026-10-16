"""统一的结构化错误（NFR-12）。

所有错误响应都是：{"code": ..., "message": ..., "details": {...}, "traceId": ...}
- 缺少字段：code=FIELD_REQUIRED，details.fields 列出缺失字段（供前端与会话代理追问）
- 违反业务规则：code=RULE_VIOLATION，details.rule 给出规则编号（如 BR-02）
- 接口尚未实现：code=NOT_IMPLEMENTED，details.task 给出任务编号
"""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from campus_common.tracing import current_trace_id


class ErrorBody(BaseModel):
    code: str = Field(description="错误码，如 FIELD_REQUIRED、RULE_VIOLATION、CONFLICT")
    message: str = Field(description="面向用户的中文说明")
    details: dict[str, Any] = Field(default_factory=dict)
    trace_id: str = Field(alias="traceId")


class AppError(Exception):
    status_code = 400
    code = "BAD_REQUEST"

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code
        self.details = details or {}


class Unauthorized(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


class Forbidden(AppError):
    status_code = 403
    code = "FORBIDDEN"


class NotFound(AppError):
    status_code = 404
    code = "NOT_FOUND"


class Conflict(AppError):
    status_code = 409
    code = "CONFLICT"


class RuleViolation(AppError):
    """违反业务规则。rule 为需求文档中的规则编号，如 BR-02、BR-M2-04。"""

    status_code = 422
    code = "RULE_VIOLATION"

    def __init__(self, rule: str, message: str, **details: Any) -> None:
        super().__init__(message, details={"rule": rule, **details})


class UpstreamError(AppError):
    """调用其他服务失败。"""

    status_code = 502
    code = "UPSTREAM_ERROR"


class NotImplementedYet(AppError):
    """接口桩：契约已定义、实现待完成。task 为 docs/tasks.md 中的任务编号。"""

    status_code = 501
    code = "NOT_IMPLEMENTED"

    def __init__(self, task: str) -> None:
        super().__init__(f"该接口尚未实现，见任务 {task}（docs/tasks.md）", details={"task": task})


def error_response(
    status_code: int, code: str, message: str, details: dict[str, Any] | None = None
) -> JSONResponse:
    body = ErrorBody(code=code, message=message, details=details or {}, traceId=current_trace_id())
    return JSONResponse(status_code=status_code, content=body.model_dump(by_alias=True))


def _field_name(loc: tuple[Any, ...]) -> str:
    parts = [str(p) for p in loc if p not in ("body", "query", "path", "header")]
    return ".".join(parts) or ".".join(str(p) for p in loc)


async def _app_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)  # noqa: S101
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def _validation_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)  # noqa: S101
    errors = [
        {"field": _field_name(tuple(e["loc"])), "type": e["type"], "message": e["msg"]}
        for e in exc.errors()
    ]
    missing = [e["field"] for e in errors if e["type"] == "missing"]
    if missing and len(missing) == len(errors):
        return error_response(
            422, "FIELD_REQUIRED", "缺少必填字段：" + "、".join(missing), {"fields": missing}
        )
    fields = sorted({e["field"] for e in errors})
    return error_response(
        422,
        "FIELD_INVALID",
        "字段不合法：" + "、".join(fields),
        {"fields": fields, "errors": errors},
    )


async def _http_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)  # noqa: S101
    codes = {401: "UNAUTHORIZED", 403: "FORBIDDEN", 404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
    return error_response(
        exc.status_code, codes.get(exc.status_code, "HTTP_ERROR"), str(exc.detail)
    )


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error)
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(StarletteHTTPException, _http_error)
    # 未捕获的异常由 tracing.TraceMiddleware 转成 500 响应
