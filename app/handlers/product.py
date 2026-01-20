import json
import uuid
from database import SessionLocal
from schemas.product import ProductCreate, ProductUpdate
from services.product import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product
)

from core.response import success, error

def create_product_handler(event):
    db = SessionLocal()
    try:
        body = json.loads(event["body"])
        data = ProductCreate(**body)

        product = create_product(db, data)
        return success(product, status_code=201)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_product_handler(event):
    db = SessionLocal()
    try:
        product_id = uuid.UUID(event["pathParameters"]["product_id"])
        product = get_product(db, product_id)

        if not product:
            return error(404, "Product not found")

        return success(product)

    except ValueError:
        return error(400, "Invalid product ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_all_products_handler(event):
    db = SessionLocal()
    try:
        products = get_all_products(db)
        return success(products)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def update_product_handler(event):
    db = SessionLocal()
    try:
        product_id = uuid.UUID(event["pathParameters"]["product_id"])
        body = json.loads(event["body"])
        data = ProductUpdate(**body)

        product = update_product(db, product_id, data)

        if not product:
            return error(404, "Product not found")

        return success(product)

    except ValueError:
        return error(400, "Invalid product ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def delete_product_handler(event):
    db = SessionLocal()
    try:
        product_id = uuid.UUID(event["pathParameters"]["product_id"])
        deleted_id = delete_product(db, product_id)

        if not deleted_id:
            return error(404, "Product not found")

        return success({"deleted_product_id": str(deleted_id)})

    except ValueError:
        return error(400, "Invalid product ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()