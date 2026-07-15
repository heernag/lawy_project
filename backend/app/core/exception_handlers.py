from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import INVALID_REQUEST
from app.core.responses import api_error


def _json_safe_errors(errors: list[dict]) -> list[dict]:
    safe_errors: list[dict] = []
    for error in errors:
        safe_error = dict(error)
        ctx = safe_error.get("ctx")
        if isinstance(ctx, dict):
            safe_error["ctx"] = {
                key: str(value) if isinstance(value, Exception) else value
                for key, value in ctx.items()
            }
        safe_errors.append(safe_error)
    return safe_errors


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=api_error(
            INVALID_REQUEST,
            "요청 값이 올바르지 않습니다.",
            details=_json_safe_errors(exc.errors()),
        ),
    )
