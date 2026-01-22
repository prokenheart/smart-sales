from sqlalchemy.orm import Session
from sqlalchemy import select, exists
from models import Price, Product
import uuid
from datetime import date
from decimal import Decimal

class NotFoundError(Exception):
    pass

def create_price(
        db: Session,
        product_id: uuid.UUID,
        price_amount: Decimal,
        price_date: date
    ) -> Price:
    if not product_exists(db, product_id):
        raise NotFoundError("Product with given ID does not exist.")
    price = Price(
        product_id=product_id,
        price_amount=price_amount,
        price_date=price_date
    )
    db.add(price)
    db.commit()
    db.refresh(price)
    return price

def get_price(db: Session, price_id: uuid.UUID) -> Price | None:
    stmt = select(Price).where(Price.price_id == price_id)
    return db.execute(stmt).scalar_one_or_none()

def price_exists(db: Session, price_id: uuid.UUID) -> bool:
    stmt = select(exists().where(Price.price_id == price_id))
    return db.execute(stmt).scalar_one()

def get_prices_by_product(db: Session, product_id: uuid.UUID) -> list[Price]:
    if not product_exists(db, product_id):
        raise NotFoundError("Product with given ID does not exist.")
    stmt = select(Price).where(Price.product_id == product_id)
    return db.execute(stmt).scalars().all()

def get_all_prices(db: Session) -> list[Price]:
    stmt = select(Price)
    return db.execute(stmt).scalars().all()

def update_price(
        db: Session,
        price_id: uuid.UUID,
        product_id: uuid.UUID | None = None,
        price_amount: Decimal | None = None,
        price_date: date | None = None
    ) -> Price:
    price = get_price(db, price_id)
    if not price:
        raise NotFoundError("Price with given ID does not exist.")

    if product_id is not None:
        if not product_exists(db, product_id):
            raise NotFoundError("Product with given ID does not exist.")            
        price.product_id = product_id
    if price_amount is not None:
        price.price_amount = price_amount
    if price_date is not None:
        price.price_date = price_date

    db.commit()
    db.refresh(price)
    return price

def delete_price(db: Session, price_id: uuid.UUID) -> uuid.UUID | bool:
    price = get_price(db, price_id)
    if not price:
        return False

    db.delete(price)
    db.commit()
    return price_id

def product_exists(db: Session, product_id: uuid.UUID) -> bool:
    stmt = select(exists().where(Product.product_id == product_id))
    return db.execute(stmt).scalar_one()