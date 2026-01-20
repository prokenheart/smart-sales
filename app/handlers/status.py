import json
import uuid
from database import SessionLocal
from schemas.status import StatusCreate, StatusUpdate
from services.status import (
    create_status,
    get_status,
    get_all_statuss,
    update_status,
    delete_status
)

from core.response import success, error

def create_status_handler(event):
    db = SessionLocal()
    try:
        body = json.loads(event["body"])
        data = StatusCreate(**body)

        status = create_status(db, data)
        return success(status, status_code=201)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_status_handler(event):
    db = SessionLocal()
    try:
        status_id = uuid.UUID(event["pathParameters"]["status_id"])
        status = get_status(db, status_id)

        if not status:
            return error(404, "Status not found")

        return success(status)

    except ValueError:
        return error(400, "Invalid status ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_all_statuss_handler(event):
    db = SessionLocal()
    try:
        statuss = get_all_statuss(db)
        return success(statuss)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()


def update_status_handler(event):
    db = SessionLocal()
    try:
        status_id = uuid.UUID(event["pathParameters"]["status_id"])
        body = json.loads(event["body"])
        data = StatusUpdate(**body)

        status = update_status(db, status_id, data)

        if not status:
            return error(404, "Status not found")

        return success(status)

    except ValueError:
        return error(400, "Invalid status ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def delete_status_handler(event):
    db = SessionLocal()
    try:
        status_id = uuid.UUID(event["pathParameters"]["status_id"])
        deleted_id = delete_status(db, status_id)

        if not deleted_id:
            return error(404, "Status not found")

        return success({"deleted_status_id": str(deleted_id)})

    except ValueError:
        return error(400, "Invalid status ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()