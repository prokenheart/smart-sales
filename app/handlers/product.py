from pydantic import ValidationError
from app.database import SessionLocal
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductIdPath
)

from app.services.product import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product,
    search_products_by_name
)

from app.core.response import success, error


def create_product_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        data = ProductCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
        product = create_product(
            db,
            data.product_name,
            data.product_description,
            data.product_quantity
        )
        response = ProductResponse.model_validate(product)
        return success(
            data=response,
            status_code=201
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_product_handler(product_id: str):
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError:
            return error(
                message="Invalid product_id",
                status_code=400
            )
    
    db = SessionLocal()
    try:
        product = get_product(db, product_id)

        if not product:
            return error(
                message="Product not found",
                status_code=404
            )
        
        response = ProductResponse.model_validate(product)

        return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def get_all_products_handler():
    db = SessionLocal()
    try:
        products = get_all_products(db)
        return success([
            ProductResponse.model_validate(product) for product in products
        ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def update_product_handler(product_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid product_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = ProductUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
        product = update_product(
            db,
            product_id,
            data.product_name,
            data.product_description,
            data.product_quantity
        )

        if not product:
            return error(
                message="Product not found",
                status_code=404
            )
        
        response = ProductResponse.model_validate(product)
        return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def delete_product_handler(product_id: str):
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
        deleted_id = delete_product(db, product_id)

        if not deleted_id:
            return error(
                message="Product not found",
                status_code=404
            )

        return success(
            data={"product_id": str(deleted_id)}
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

    finally:
        db.close()

def search_products_handler(query: str):
    if not query or not query.strip():
        return error(
            message="Query parameter is required and cannot be empty",
            status_code=400
        )
    db = SessionLocal()
    try:        
        products = search_products_by_name(db, query)

        return success([
            ProductResponse.model_validate(product) for product in products
        ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )
    
    finally:
        db.close()
