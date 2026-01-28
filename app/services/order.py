from sqlalchemy.orm import Session
from sqlalchemy import select, exists
from app.models import Order, User, Customer, Status
import uuid
from datetime import date, datetime, timedelta

class NotFoundError(Exception):
    pass

def create_order(
        db: Session,
        customer_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Order:

    customer = get_customer(db, customer_id)
    user = get_user(db, user_id)
    status = get_default_status(db)

    order = Order(
        customer=customer,
        user=user,
        status=status,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: uuid.UUID) -> Order | None:
    stmt = select(Order).where(Order.order_id == order_id)
    return db.execute(stmt).scalar_one_or_none()

def get_orders_by_user(db: Session, user_id: uuid.UUID) -> list[Order]:
    if not user_exists(db, user_id):
        raise NotFoundError("User with given ID does not exist.")
    stmt = select(Order).where(Order.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_orders_by_customer(db: Session, customer_id: uuid.UUID) -> list[Order]:
    if not customer_exists(db, customer_id):
        raise NotFoundError("Customer with given ID does not exist.")
    stmt = select(Order).where(Order.customer_id == customer_id)
    return db.execute(stmt).scalars().all()

def get_orders_by_status(db: Session, status_code: str) -> list[Order]:
    status = get_status_by_code(db, status_code)
    stmt = select(Order).where(Order.status_id == status.status_id)
    return db.execute(stmt).scalars().all()

def get_all_orders(db: Session) -> list[Order]:
    stmt = select(Order)
    return db.execute(stmt).scalars().all()

def update_order_status(
        db: Session,
        order_id: uuid.UUID,
        status_id: uuid.UUID
    ) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None
    
    status = get_status(db, status_id)
    order.status = status

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: uuid.UUID) -> uuid.UUID | bool:
    order = get_order(db, order_id)
    if not order:
        return False

    db.delete(order)
    db.commit()
    return order_id

def get_user(db: Session, user_id: uuid.UUID) -> User:
    user = db.get(User, user_id)
    if not user:
        raise NotFoundError("User with given ID does not exist.")
    return user

def get_customer(db: Session, customer_id: uuid.UUID) -> Customer:
    customer = db.get(Customer, customer_id)
    if not customer:
        raise NotFoundError("Customer with given ID does not exist.")
    return customer

def get_status(db: Session, status_id: uuid.UUID) -> Status:
    status = db.get(Status, status_id)
    if not status:
        raise NotFoundError("Status with given ID does not exist.")
    return status

def get_status_by_code(db: Session, status_code: str) -> Status:
    stmt = select(Status).where(Status.status_code == status_code)
    status = db.execute(stmt).scalar_one_or_none()
    if not status:
        raise NotFoundError("Status with given code does not exist.")
    return status

def get_default_status(db: Session) -> Status:
    stmt = select(Status).where(Status.status_code == 'PENDING')
    status = db.execute(stmt).scalar_one_or_none()
    if not status:
        raise NotFoundError("Default status not found.")
    return status

def user_exists(db: Session, user_id: uuid.UUID) -> bool:
    stmt = select(exists().where(User.user_id == user_id))
    return db.execute(stmt).scalar()

def customer_exists(db: Session, customer_id: uuid.UUID) -> bool:
    stmt = select(exists().where(Customer.customer_id == customer_id))
    return db.execute(stmt).scalar()

def status_exists(db: Session, status_code: str) -> bool:
    stmt = select(exists().where(Status.status_code == status_code))
    return db.execute(stmt).scalar()

def get_orders_by_date(db: Session, order_date: date) -> list[Order]:
    start = datetime.combine(order_date, datetime.min.time())
    end = start + timedelta(days=1)

    stmt = (
        select(Order)
        .where(Order.order_date >= start)
        .where(Order.order_date < end)
    )

    return db.execute(stmt).scalars().all()