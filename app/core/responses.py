from typing import Any


def success_response(data: Any = None, message: str = "Success") -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str) -> dict:
    return {
        "success": False,
        "message": message,
        "data": None,
    }
