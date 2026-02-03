from aws_lambda_powertools.event_handler import Response
from typing import Any
from enum import Enum

def success(data: Any = None, status_code: int = 200):
    return Response(
        status_code=status_code,
        content_type="application/json",
        body={
            "data": data
        }
    )


def error(message: str, status_code: int = 400, details: Any = None):
    return Response(
        status_code=status_code,
        content_type="application/json",
        body={
            "message": message,
            "details": details
        }
    )

class StatusCode (int, Enum):
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500