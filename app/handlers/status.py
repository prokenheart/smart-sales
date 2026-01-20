from pydantic import ValidationError
from database import SessionLocal
from logger import logger
from schemas.status import (
    StatusCreate,
    StatusIdPath,
    StatusResponse,
    StatusUpdate
)

from services.status import (
    create_status,
    get_status,
    get_all_statuses,
    update_status,
    delete_status
)

from core.response import success, error

def create_status_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        data = StatusCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
        status = create_status(
            db,
            data.status_name
        )
        response = StatusResponse.model_validate(status)
        return success(
            data=response,
            status_code=201
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_status_handler(status_id: str):
    try:
        status_id = StatusIdPath.model_validate({"status_id": status_id}).status_id
    except ValidationError:
            return error(
                message="Invalid status_id",
                status_code=400
            )
    
    db = SessionLocal()
    try:
        status = get_status(db, status_id)

        if not status:
            return error(
                message="Status not found",
                status_code=404
            )
        
        response = StatusResponse.model_validate(status)

        return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_all_statuses_handler():
    db = SessionLocal()
    try:
        statuses = get_all_statuses(db)
        return success([
            StatusResponse.model_validate(status) for status in statuses
        ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def update_status_handler(status_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        status_id = StatusIdPath.model_validate({"status_id": status_id}).status_id
    except ValidationError as e:
        return error(
            message="Invalid status_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = StatusUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
        status = update_status(
            db,
            status_id,
            data.status_name
        )

        if not status:
            return error(
                message="Status not found",
                status_code=404
            )
        
        response = StatusResponse.model_validate(status)
        return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def delete_status_handler(status_id: str):
    try:
        status_id = StatusIdPath.model_validate({"status_id": status_id}).status_id
    except ValidationError as e:
        return error(
            message="Invalid status_id",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
        deleted_id = delete_status(db, status_id)

        if not deleted_id:
            return error(
                message="Status not found",
                status_code=404
            )

        return success(
            data={"status_id": str(deleted_id)}
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()