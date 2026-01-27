from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Customer
import uuid

def create(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_by_id(db: Session, customer_id: uuid.UUID) -> Customer | None:
    stmt = select(Customer).where(Customer.customer_id == customer_id)
    return db.execute(stmt).scalar_one_or_none()

def get_by_email(db: Session, email: str) -> Customer | None:
    stmt = select(Customer).where(Customer.customer_email == email)
    return db.execute(stmt).scalar_one_or_none()

def get_all(db: Session) -> list[Customer]:
    stmt = select(Customer)
    return db.execute(stmt).scalars().all()

def update(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def delete(db: Session, customer: Customer):
    db.delete(customer)
    db.commit()

def search_by_name(db: Session, keyword: str):
    stmt = select(Customer).where(Customer.customer_name.ilike(f"%{keyword}%"))
    return db.execute(stmt).scalars().all()

def search_by_email(db: Session, keyword: str):
    stmt = select(Customer).where(Customer.customer_email.ilike(f"%{keyword}%"))
    return db.execute(stmt).scalars().all()

def search_by_phone(db: Session, keyword: str):
    stmt = select(Customer).where(Customer.customer_phone.ilike(f"%{keyword}%"))
    return db.execute(stmt).scalars().all()
