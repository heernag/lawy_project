from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import INVALID_REQUEST
from app.core.responses import api_error


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=api_error(
            INVALID_REQUEST,
            "요청 값이 올바르지 않습니다.",
            details=exc.errors(),
        ),
    )
