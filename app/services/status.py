from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Status
import uuid


def create_status(
        db: Session,
        status_name: str
    ) -> Status:
    status = Status(
        status_name=status_name,
    )
    db.add(status)
    db.commit()
    db.refresh(status)
    return status

def get_status(db: Session, status_id: uuid.UUID) -> Status | None:
    stmt = select(Status).where(Status.status_id == status_id)
    return db.execute(stmt).scalar_one_or_none()

def get_all_statuses(db: Session) -> list[Status]:
    stmt = select(Status)
    return db.execute(stmt).scalars().all()

def update_status(
        db: Session,
        status_id: uuid.UUID,
        status_name: str
    ) -> Status | None:
    status = get_status(db, status_id)
    if not status:
        return None

    if status_name:
        status.status_name = status_name

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