from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, exists, func, and_, or_
from sqlalchemy.sql import Select
from app.models import Order, User, Customer, Status
import uuid
from datetime import datetime
from app.core.logger import logger
from app.schemas.order import OrderFilterQuery, OrderPaginationResponse


class NotFoundError(Exception):
    pass


def create_order(db: Session, customer_id: uuid.UUID, user_id: uuid.UUID) -> Order:

    customer = get_customer(db, customer_id)
    user = get_user(db, user_id)
    status = get_default_status(db)

    order = Order(
        customer_id=customer.customer_id,
        user_id=user.user_id,
        status_id=status.status_id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: uuid.UUID) -> Order | None:
    stmt = select(Order).where(Order.order_id == order_id)
    return db.execute(stmt).scalar_one_or_none()


def _apply_filters(stmt: Select, db: Session, query: OrderFilterQuery) -> Select:
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
        start = datetime.combine(query.order_date, datetime.min.time())
        end = datetime.combine(query.order_date, datetime.max.time())
        stmt = stmt.where(Order.order_date >= start, Order.order_date <= end)

    return stmt


def _apply_page_number_pagination(
    query: OrderFilterQuery, stmt: Select, limit: int
) -> Select:
    if query.page:
        stmt = stmt.order_by(Order.order_date.desc(), Order.order_id.desc())
        stmt = stmt.offset((query.page - 1) * limit)
    return stmt


def _apply_cursor_pagination(
    stmt: Select, query: OrderFilterQuery, is_prev: bool
) -> Select:
    if query.cursor_date:
        if is_prev:
            stmt = stmt.where(
                or_(
                    Order.order_date > query.cursor_date,
                    and_(
                        Order.order_date == query.cursor_date,
                        Order.order_id > query.cursor_id,
                    ),
                )
            ).order_by(Order.order_date.asc(), Order.order_id.asc())
        else:
            stmt = stmt.where(
                or_(
                    Order.order_date < query.cursor_date,
                    and_(
                        Order.order_date == query.cursor_date,
                        Order.order_id < query.cursor_id,
                    ),
                )
            ).order_by(Order.order_date.desc(), Order.order_id.desc())

    return stmt


def _get_paging_flags(
    cursor_date: datetime | None,
    cursor_id: uuid.UUID | None,
    is_prev: bool,
    has_more: bool,
    page: int | None = None,
) -> tuple[bool, bool]:
    if cursor_date is None or cursor_id is None:
        if page is not None and page > 1:
            return True, has_more
        return False, has_more

    if is_prev:
        return has_more, True

    return True, has_more


def _count_orders(db: Session, query: OrderFilterQuery) -> int:
    stmt = select(func.count(Order.order_id))
    stmt = _apply_filters(stmt, db, query)
    return db.execute(stmt).scalar_one()


def _get_current_page(query: OrderFilterQuery, is_prev: bool) -> int:
    if query.cursor_date and query.cursor_id:
        if is_prev:
            return query.current_page - 1
        return query.current_page + 1

    if query.page:
        return query.page

    return 1


LIMIT = 20


def get_orders(
    db: Session,
    query: OrderFilterQuery,
) -> OrderPaginationResponse:

    limit = LIMIT

    stmt = select(Order)
    stmt = stmt.options(joinedload(Order.status))
    stmt = stmt.options(joinedload(Order.customer))
    stmt = stmt.options(joinedload(Order.user))
    if query.page is None and query.cursor_date is None:
        stmt = stmt.order_by(Order.order_date.desc(), Order.order_id.desc())

    stmt = _apply_filters(stmt, db, query)

    stmt = _apply_page_number_pagination(query, stmt, limit)

    is_prev = query.cursor_date is not None and query.direction == "prev"
    stmt = _apply_cursor_pagination(stmt, query, is_prev)
    stmt = stmt.limit(limit + 1)

    rows = db.execute(stmt).scalars().all()

    has_more = len(rows) > limit
    orders = rows[:limit]

    if is_prev:
        orders.reverse()

    has_prev, has_next = _get_paging_flags(
        query.cursor_date, query.cursor_id, is_prev, has_more, query.page
    )

    prev_cursor_date = None
    prev_cursor_id = None
    next_cursor_date = None
    next_cursor_id = None

    if orders:
        if has_prev:
            prev_cursor_date = orders[0].order_date
            prev_cursor_id = orders[0].order_id
        if has_next:
            next_cursor_date = orders[-1].order_date
            next_cursor_id = orders[-1].order_id

    total_count = _count_orders(db, query)
    total_pages = (total_count + limit - 1) // limit
    current_page = _get_current_page(query, is_prev)

    order_pagination_response = OrderPaginationResponse(
        orders=orders,
        prev_cursor_date=prev_cursor_date,
        prev_cursor_id=prev_cursor_id,
        next_cursor_date=next_cursor_date,
        next_cursor_id=next_cursor_id,
        total_pages=total_pages,
        current_page=current_page,
        total_orders=total_count
    )

    return order_pagination_response


def update_order_status(
    db: Session, order_id: uuid.UUID, status_code: str
) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None

    old_status = get_status(db, order.status_id)

    status = get_status_by_code(db, status_code)
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
            "new_status": str(status.status_code),
        },
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
    stmt = select(Status).where(Status.status_code == "PENDING")
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
    db: Session, order_id: uuid.UUID, attachment_url: str
) -> Order | None:
    order = get_order(db, order_id)
    if not order:
        return None

    order.order_attachment = attachment_url

    db.add(order)
    db.commit()
    db.refresh(order)
    return order
