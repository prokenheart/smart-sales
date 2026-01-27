from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Customer
from repositories import customer as repo
import uuid

class DuplicateEmailError(Exception):
    pass

def create_customer(
    db: Session,
    customer_name: str,
    customer_email: str,
    customer_phone: str
) -> Customer:
    
    if repo.get_by_email(db, customer_email):
        raise DuplicateEmailError("Email already exists")
        
    customer = Customer(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone
    )

    try:
        return repo.create(db, customer)
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already exists")

def get_customer(db: Session, customer_id: uuid.UUID) -> Customer | None:
    return repo.get_by_id(db, customer_id)

def get_customer_by_email(db: Session, customer_email: str) -> Customer | None:
    return repo.get_by_email(db, customer_email)

def get_all_customers(db: Session) -> list[Customer]:
    return repo.get_all(db)

def update_customer(
        db: Session,
        customer_id: uuid.UUID,
        customer_name: str | None = None,
        customer_email: str | None = None,
        customer_phone: str | None = None
    ) -> Customer | None:
    customer = repo.get_by_id(db, customer_id)
    if not customer:
        return None

    if customer_email and customer_email != customer.customer_email:
        if repo.get_by_email(db, customer_email):
            raise DuplicateEmailError("Email already exists")
        customer.customer_email = customer_email

    if customer_name:
        customer.customer_name = customer_name
    if customer_phone:
        customer.customer_phone = customer_phone

    try:
        return repo.update(db, customer)
    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError("Email already exists")

def delete_customer(db: Session, customer_id: uuid.UUID) -> uuid.UUID | None:
    customer = repo.get_by_id(db, customer_id)
    if not customer:
        return None

    repo.delete(db, customer)
    return customer_id

def search_customers_by_name(db: Session, name_query: str) -> list[Customer]:
    return repo.search_by_name(db, name_query)

def search_customers_by_email(db: Session, email_query: str) -> list[Customer]:
    return repo.search_by_email(db, email_query)

def search_customers_by_phone(db: Session, phone_query: str) -> list[Customer]:
    return repo.search_by_phone(db, phone_query)