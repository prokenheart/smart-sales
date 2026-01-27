from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Status
import uuid

def get_status(db: Session, status_id: uuid.UUID) -> Status | None:
    stmt = select(Status).where(Status.status_id == status_id)
    return db.execute(stmt).scalar_one_or_none()

def get_status_by_code(db: Session, status_code: str) -> Status | None:
    stmt = select(Status).where(Status.status_code == status_code)
    return db.execute(stmt).scalar_one_or_none()

def get_all_statuses(db: Session) -> list[Status]:
    stmt = select(Status)
    return db.execute(stmt).scalars().all()