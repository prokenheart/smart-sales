from pydantic import ValidationError
from app.database import get_db
from app.schemas.status import (
    StatusIdPath,
    StatusCode,
    StatusResponse
)

from app.services.status import (
    get_status,
    get_status_by_code,
    get_all_statuses,
)

from app.core.response import success, error, ResponseStatusCode, errors_from_validation_error, Response

def get_status_handler(status_id: str) -> Response:
    try:
        status_id = StatusIdPath.model_validate({"status_id": status_id}).status_id
    except ValidationError as e:
            return error(
                message="Invalid status_id",
                status_code=ResponseStatusCode.BAD_REQUEST,
                details=errors_from_validation_error(e)
            )
    
    try:
        with get_db() as db:
            status = get_status(db, status_id)

            if not status:
                return error(
                    message="Status not found",
                    status_code=ResponseStatusCode.NOT_FOUND
                )
            
            response = StatusResponse.model_validate(status)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_status_by_code_handler(status_code: str) -> Response:
    try:
        status_code = StatusCode.model_validate({"status_code": status_code}).status_code
    except ValidationError as e:
        return error(
            message="Invalid status code",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        with get_db() as db:
            status = get_status_by_code(db, status_code)
            
            if not status:
                return error(
                    message="Status not found",
                    status_code=ResponseStatusCode.NOT_FOUND
                )
            
            response = StatusResponse.model_validate(status)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_all_statuses_handler() -> Response:
    try:
        with get_db() as db:
            statuses = get_all_statuses(db)
            return success([
                StatusResponse.model_validate(status) for status in statuses
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )