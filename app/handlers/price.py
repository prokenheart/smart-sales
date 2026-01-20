import json
import uuid
from database import SessionLocal
from schemas.price import PriceCreate, PriceUpdate
from services.price import (
    create_price,
    get_price,
    get_prices_by_product,
    get_all_prices,
    update_price,
    delete_price
)

from core.response import success, error

def create_price_handler(event):
    db = SessionLocal()
    try:
        body = json.loads(event["body"])
        data = PriceCreate(**body)

        price = create_price(db, data)
        return success(price, price_code=201)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_price_handler(event):
    db = SessionLocal()
    try:
        price_id = uuid.UUID(event["pathParameters"]["price_id"])
        price = get_price(db, price_id)

        if not price:
            return error(404, "Price not found")

        return success(price)

    except ValueError:
        return error(400, "Invalid price ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_price_by_product_handler(event):
    db = SessionLocal()
    try:
        product_id = uuid.UUID(event["pathParameters"]["product_id"])
        prices = get_prices_by_product(db, product_id)

        return success(prices)

    except ValueError:
        return error(400, "Invalid product ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_all_prices_handler(event):
    db = SessionLocal()
    try:
        prices = get_all_prices(db)
        return success(prices)

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()


def update_price_handler(event):
    db = SessionLocal()
    try:
        price_id = uuid.UUID(event["pathParameters"]["price_id"])
        body = json.loads(event["body"])
        data = PriceUpdate(**body)

        price = update_price(db, price_id, data)

        if not price:
            return error(404, "Price not found")

        return success(price)

    except ValueError:
        return error(400, "Invalid price ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def delete_price_handler(event):
    db = SessionLocal()
    try:
        price_id = uuid.UUID(event["pathParameters"]["price_id"])
        deleted_id = delete_price(db, price_id)

        if not deleted_id:
            return error(404, "Price not found")

        return success({"deleted_price_id": str(deleted_id)})

    except ValueError:
        return error(400, "Invalid price ID format")

    except Exception as e:
        return error(500, "Internal server error")

    finally:
        db.close()

def get_prices_collection_handler(event):
    query = event.get("queryStringParameters") or {}

    if "product_id" in query:
        return get_price_by_product_handler(event)
    
    return get_all_prices_handler(event)