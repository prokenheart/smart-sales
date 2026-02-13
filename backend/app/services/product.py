from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models import Product
import uuid


def create_product(
    db: Session, product_name: str, product_description: str, product_quantity: int
) -> Product:
    product = Product(
        product_name=product_name,
        product_description=product_description,
        product_quantity=product_quantity,
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


def update_product(
    db: Session,
    product_id: uuid.UUID,
    product_name: str | None = None,
    product_description: str | None = None,
    product_quantity: int | None = None,
) -> Product | None:
    product = get_product(db, product_id)
    if not product:
        return None

    if product_name:
        product.product_name = product_name
    if product_description:
        product.product_description = product_description
    if product_quantity:
        product.product_quantity = product_quantity

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: uuid.UUID) -> uuid.UUID | None:
    product = get_product(db, product_id)
    if not product:
        return None

    db.delete(product)
    db.commit()
    return product_id



def search_products_by_name(db: Session, name_query: str) -> list[Product]:
    stmt = (
        select(Product)
        .where(Product.product_name.ilike(f"%{name_query}%"))
        .options(joinedload(Product.prices))
    )

    products = db.execute(stmt).unique().scalars().all()

    for p in products:
        p.prices = p.prices[:1]

    return products
