from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Status
from schemas.status import StatusCreate, StatusUpdate
import uuid


def create_status(db: Session, data: StatusCreate) -> Status:
    status = Status(
        status_name=data.status_name,
    )
    db.add(status)
    db.commit()
    db.refresh(status)
    return status

def get_status(db: Session, status_id: uuid.UUID) -> Status | None:
    stmt = select(Status).where(Status.status_id == status_id)
    return db.execute(stmt).scalar_one_or_none()

def get_all_statuss(db: Session) -> list[Status]:
    stmt = select(Status)
    return db.execute(stmt).scalars().all()

def update_status(db: Session, status_id: uuid.UUID, data: StatusUpdate) -> Status | None:
    status = get_status(db, status_id)
    if not status:
        return None

    if data.status_name:
        status.status_name = data.status_name

    db.add(status)
    db.commit()
    db.refresh(status)
    return status

def delete_status(db: Session, status_id: uuid.UUID) -> uuid.UUID:
    status = get_status(db, status_id)
    if not status:
        return False

    db.delete(status)
    db.commit()
    return status_id