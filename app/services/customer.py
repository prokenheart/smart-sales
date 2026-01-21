from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Customer
import uuid

class DuplicateEmailError(Exception):
    pass

def create_customer(
        db: Session,
        customer_name: str,
        customer_email: str,
        customer_phone: str
    ) -> Customer:
    if get_customer_by_email(db, customer_email):
        raise DuplicateEmailError("Email already exists")
        
    customer = Customer(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone
    )

    db.add(customer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already exists")
    db.refresh(customer)
    return customer

def get_customer(db: Session, customer_id: uuid.UUID) -> Customer | None:
    stmt = select(Customer).where(Customer.customer_id == customer_id)
    return db.execute(stmt).scalar_one_or_none()

def get_customer_by_email(db: Session, customer_email: str) -> Customer | None:
    stmt = select(Customer).where(Customer.customer_email == customer_email)
    return db.execute(stmt).scalar_one_or_none()

def get_all_customers(db: Session) -> list[Customer]:
    stmt = select(Customer)
    return db.execute(stmt).scalars().all()

def update_customer(
        db: Session,
        customer_id: uuid.UUID,
        customer_name: str | None = None,
        customer_email: str | None = None,
        customer_phone: str | None = None
    ) -> Customer | None:
    customer = get_customer(db, customer_id)
    if not customer:
        return None

    if customer_email and customer_email != customer.customer_email:
        if get_customer_by_email(db, customer_email):
            raise DuplicateEmailError("Email already exists")
        customer.customer_email = customer_email

    if customer_name:
        customer.customer_name = customer_name
    if customer_phone:
        customer.customer_phone = customer_phone

    db.add(customer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already exists")
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: uuid.UUID) -> uuid.UUID:
    customer = get_customer(db, customer_id)
    if not customer:
        return False

    db.delete(customer)
    db.commit()
    return customer_id

def search_customers_by_name(db: Session, name_query: str) -> list[Customer]:
    stmt = select(Customer).where(Customer.customer_name.ilike(f"%{name_query}%"))
    return db.execute(stmt).scalars().all()

def search_customers_by_email(db: Session, email_query: str) -> list[Customer]:
    stmt = select(Customer).where(Customer.customer_email.ilike(f"%{email_query}%"))
    return db.execute(stmt).scalars().all()

def search_customers_by_phone(db: Session, phone_query: str) -> list[Customer]:
    stmt = select(Customer).where(Customer.customer_phone.ilike(f"%{phone_query}%"))
    return db.execute(stmt).scalars().all()