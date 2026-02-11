from aws_lambda_powertools.event_handler import Response
from typing import Any
from pydantic import ValidationError, BaseModel


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "http://localhost:5173",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
}


def success(data: Any = None, status_code: int = 200) -> Response:
    if isinstance(data, BaseModel):
        data = data.model_dump(mode="json", by_alias=True)
    elif isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
        data = [item.model_dump(mode="json", by_alias=True) for item in data]
    return Response(
        status_code=status_code,
        content_type="application/json",
        headers=CORS_HEADERS,
        body=data,
    )


def error(message: str, status_code: int = 400, details: Any = None) -> Response:
    return Response(
        status_code=status_code,
        content_type="application/json",
        headers=CORS_HEADERS,
        body={"message": message, "details": details},
    )


def errors_from_validation_error(e: ValidationError) -> list[dict[str, Any]]:
    errors = []
    for err in e.errors():
        error = {
            "type": err.get("type", ""),
            "loc": err.get("loc", []),
            "msg": err.get("msg", ""),
            "input": err.get("input", ""),
        }
        errors.append(error)
    return errors
