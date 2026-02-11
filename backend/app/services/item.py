from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, exists
from app.models import Item, Product, Order, Price
from app.schemas.item import ItemBase
import uuid
from datetime import date
from decimal import Decimal
from dataclasses import dataclass


class NotFoundError(Exception):
    pass


class NotEnoughError(Exception):
    pass


@dataclass
class CreateItemResult:
    items: list[Item]
    total_price: Decimal


def _create_item(
    db: Session, order_id: uuid.UUID, product_id: uuid.UUID, item_quantity: int
) -> Item:

    item_price = get_price(db, product_id, date.today()).price_amount
    item = Item(
        order_id=order_id,
        product_id=product_id,
        item_quantity=item_quantity,
        item_price=item_price,
    )
    db.add(item)
    return item


def _create_list_of_item(
    db: Session, order_id: uuid.UUID, list_items: list[ItemBase]
) -> CreateItemResult:

    total_price = Decimal(0)
    product_cache: dict[uuid.UUID, Product] = {}
    created_items: list[Item] = []

    for item in list_items:
        if item.product_id not in product_cache:
            product_cache[item.product_id] = get_product(db, item.product_id)
        product = product_cache[item.product_id]
        decrease_product_quantity(product, item.item_quantity)
        new_item = _create_item(db, order_id, item.product_id, item.item_quantity)
        total_price += new_item.item_price * new_item.item_quantity

        created_items.append(new_item)

    return CreateItemResult(items=created_items, total_price=total_price)


def get_item(
    db: Session, order_item: uuid.UUID, product_item: uuid.UUID
) -> Item | None:
    stmt = select(Item).where(
        Item.product_id == product_item, Item.order_id == order_item
    )
    return db.execute(stmt).scalar_one_or_none()


def get_items_by_order(db: Session, order_id: uuid.UUID) -> list[Item]:
    if not order_exists(db, order_id):
        raise NotFoundError("Order with given ID does not exist.")
    stmt = (
        select(Item).options(joinedload(Item.product)).where(Item.order_id == order_id)
    )
    return db.execute(stmt).scalars().all()


def get_all_items(db: Session) -> list[Item]:
    stmt = select(Item)
    return db.execute(stmt).scalars().all()


def update_list_of_item(
    db: Session, order_id: uuid.UUID, list_items: list[ItemBase]
) -> list[Item]:
    order = get_order(db, order_id)
    order.ensure_items_can_be_modified()

    try:
        _delete_list_of_item(db, order_id)

        result = _create_list_of_item(db, order_id, list_items)

        order.order_total = result.total_price
        db.commit()
        for item in result.items:
            db.refresh(item)

        return result.items
    except Exception:
        db.rollback()
        raise


def _delete_list_of_item(db: Session, order_id: uuid.UUID) -> None:

    list_items = get_items_by_order(db, order_id)
    product_cache: dict[uuid.UUID, Product] = {}

    for item in list_items:
        if item.product_id not in product_cache:
            product_cache[item.product_id] = get_product(db, item.product_id)
        product = product_cache[item.product_id]
        increase_product_quantity(product, item.item_quantity)
        db.delete(item)


def get_product(db: Session, product_id: uuid.UUID) -> Product:
    product = db.get(Product, product_id)
    if not product:
        raise NotFoundError("Product with given ID does not exist.")
    return product


def get_order(db: Session, order_id: uuid.UUID) -> Order:
    order = db.get(Order, order_id)
    if not order:
        raise NotFoundError("Order with given ID does not exist.")
    return order


def order_exists(db: Session, order_id: uuid.UUID) -> bool:
    stmt = select(exists().where(Order.order_id == order_id))
    return db.execute(stmt).scalar()


def get_price(db: Session, product_id: uuid.UUID, price_date: date) -> Price:
    stmt = (
        select(Price)
        .where(Price.product_id == product_id, Price.price_date <= price_date)
        .order_by(Price.price_date.desc())
        .limit(1)
    )
    price = db.execute(stmt).scalar_one_or_none()
    if not price:
        raise NotFoundError("Price for given product and date does not exist.")
    return price


def decrease_product_quantity(product: Product, amount: int) -> None:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if product.product_quantity < amount:
        raise NotEnoughError(
            f"Product with ID: {product.product_id} does not have sufficient quantity."
        )

    product.product_quantity -= amount


def increase_product_quantity(product: Product, amount: int) -> None:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    product.product_quantity += amount
