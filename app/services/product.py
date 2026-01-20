from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Product
from schemas.product import ProductCreate, ProductUpdate
import uuid


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(
        product_name=data.product_name,
        product_description=data.product_description,
        product_quantity=data.product_quantity
    )


    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: uuid.UUID) -> Product | None:
    stmt = select(Product).where(Product.product_id == product_id)
    return db.execute(stmt).scalar_one_or_none()

def get_all_products(db: Session) -> list[Product]:
    stmt = select(Product)
    return db.execute(stmt).scalars().all()

def update_product(db: Session, product_id: uuid.UUID, data: ProductUpdate) -> Product | None:
    product = get_product(db, product_id)
    if not product:
        return None

    if data.product_name:
        product.product_name = data.product_name
    if data.product_description:
        product.product_description = data.product_description
    if data.product_quantity:
        product.product_quantity = data.product_quantity

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: uuid.UUID) -> uuid.UUID:
    product = get_product(db, product_id)
    if not product:
        return False

    db.delete(product)
    db.commit()
    return product_id