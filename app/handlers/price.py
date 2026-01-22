from pydantic import ValidationError
from database import SessionLocal
from logger import logger
from schemas.price import (
    PriceCreate,
    PriceIdPath,
    PriceResponse,
    PriceUpdate
)

from schemas.product import ProductIdPath

from services.price import (
    create_price,
    get_price,
    get_prices_by_product,
    get_all_prices,
    update_price,
    delete_price,
    NotFoundError
)

from core.response import success, error

def create_price_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        data = PriceCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
        price = create_price(
            db,
            data.product_id,
            data.price_amount,
            data.price_date
        )

        response = PriceResponse.model_validate(price)
        return success(
            data=response,
            status_code=201
        )
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_price_handler(price_id: str):
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError:
            return error(
                message="Invalid price_id",
                status_code=400
            )
    
    db = SessionLocal()
    try:
        price = get_price(db, price_id)
        if not price:
            return error(
                message="Price not found",
                status_code=404
            )
        
        response = PriceResponse.model_validate(price)

        return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_all_prices_handler():
    db = SessionLocal()
    try:
        prices = get_all_prices(db)
        return success([
            PriceResponse.model_validate(price) for price in prices
        ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_prices_by_product_handler(product_id: str):
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid product_id",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
        prices = get_prices_by_product(db, product_id)
        return success([
            PriceResponse.model_validate(price) for price in prices
        ])
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def update_price_handler(price_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError as e:
        return error(
            message="Invalid price_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = PriceUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
        price = update_price(
            db,
            price_id,
            data.product_id,
            data.price_amount,
            data.price_date
        )
        
        response = PriceResponse.model_validate(price)
        return success(response)
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=404
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def delete_price_handler(price_id: str):
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError as e:
        return error(
            message="Invalid price_id",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
        deleted_id = delete_price(db, price_id)

        if not deleted_id:
            return error(
                message="Price not found",
                status_code=404
            )

        return success(
            data={"price_id": str(deleted_id)}
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()