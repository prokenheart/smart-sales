from aws_lambda_powertools.event_handler import Response
from typing import Any


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
