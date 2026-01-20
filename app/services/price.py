from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Price
import uuid


def create_price(
        db: Session,
        product_id: str,
        price_amount: str,
        price_date: str
    ) -> Price:
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

def get_prices_by_product(db: Session, product_id: uuid.UUID) -> list[Price]:
    stmt = select(Price).where(Price.product_id == product_id)
    return db.execute(stmt).scalars().all()

def get_all_prices(db: Session) -> list[Price]:
    stmt = select(Price)
    return db.execute(stmt).scalars().all()

def update_price(
        db: Session,
        price_id: uuid.UUID,
        product_id: str,
        price_amount: str,
        price_date: str
    ) -> Price | None:
    price = get_price(db, price_id)
    if not price:
        return None

    if product_id:
        price.product_id = product_id
    if price_amount:
        price.price_amount = price_amount
    if price_date:
        price.price_date = price_date

    db.add(price)
    db.commit()
    db.refresh(price)
    return price

def delete_price(db: Session, price_id: uuid.UUID) -> uuid.UUID:
    price = get_price(db, price_id)
    if not price:
        return False

    db.delete(price)
    db.commit()
    return price_id