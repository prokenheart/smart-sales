from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, exists
from app.models import Order, User, Customer, Status
import uuid
from datetime import datetime
from app.core.logger import logger
from app.schemas.order import OrderFilterQuery

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
        customer_id=customer.customer_id,
        user_id=user.user_id,
        status_id=status.status_id
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: uuid.UUID) -> Order | None:
    stmt = select(Order).where(Order.order_id == order_id)
    return db.execute(stmt).scalar_one_or_none()

LIMIT = 20

def get_orders(
    db: Session,
    query: OrderFilterQuery,
) -> tuple[list[Order], datetime | None, datetime | None]:

    limit = LIMIT

    stmt = select(Order).options(joinedload(Order.status))

    if query.user_id:
        if not user_exists(db, query.user_id):
            raise NotFoundError("User with given ID does not exist.")
        stmt = stmt.where(Order.user_id == query.user_id)

    if query.customer_id:
        if not customer_exists(db, query.customer_id):
            raise NotFoundError("Customer with given ID does not exist.")
        stmt = stmt.where(Order.customer_id == query.customer_id)

    if query.status_code:
        status = get_status_by_code(db, query.status_code)
        stmt = stmt.where(Order.status_id == status.status_id)

    if query.order_date:
        stmt = stmt.where(
            Order.order_date >= datetime.combine(query.order_date, datetime.min.time()),
            Order.order_date <= datetime.combine(query.order_date, datetime.max.time()),
        )

    is_prev = query.direction == "prev"

    if query.cursor:
        if is_prev:
            stmt = stmt.where(Order.order_date > query.cursor)
        else:
            stmt = stmt.where(Order.order_date < query.cursor)

    stmt = stmt.order_by(
        Order.order_date.asc() if is_prev else Order.order_date.desc()
    )

    stmt = stmt.limit(limit + 1)

    rows = db.execute(stmt).scalars().all()

    has_more = len(rows) > limit
    orders = rows[:limit]

    if is_prev:
        orders.reverse()

    has_next = False
    has_prev = False

    if query.cursor is None:
        # trang đầu
        has_prev = False
        has_next = has_more
    else:
        if is_prev:
            has_prev = has_more
            has_next = True
        else:
            has_prev = True
            has_next = has_more

    next_cursor = None
    prev_cursor = None

    if orders:
        if has_prev:
            prev_cursor = orders[0].order_date
        if has_next:
            next_cursor = orders[-1].order_date

    return orders, next_cursor, prev_cursor

def update_order_status(
        db: Session,
        order_id: uuid.UUID,
        status_id: uuid.UUID
    ) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None
    
    old_status = get_status(db, order.status_id)
    
    status = get_status(db, status_id)
    order.status_id = status.status_id

    db.add(order)
    db.commit()
    db.refresh(order)

    logger.info(
        "order_status_changed",
        extra={
            "order_id": str(order.order_id),
            "user_id": str(order.user_id),
            "old_status": str(old_status.status_code),
            "new_status": str(status.status_code)
        }
    )

    return order

def delete_order(db: Session, order_id: uuid.UUID) -> uuid.UUID | None:
    order = get_order(db, order_id)
    if not order:
        return None

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

def update_order_attachment_url(
        db: Session,
        order_id: uuid.UUID,
        attachment_url: str
    ) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None

    order.order_attachment = attachment_url

    db.add(order)
    db.commit()
    db.refresh(order)
    return order