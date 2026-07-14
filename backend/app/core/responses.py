from typing import Any


def api_success(data: Any) -> dict[str, Any]:
    return {"success": True, "data": data, "error": None}


def api_error(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {"code": code, "message": message, "details": details},
    }
