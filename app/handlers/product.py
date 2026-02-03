from pydantic import ValidationError
from app.database import get_db
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

from app.core.response import success, error, ResponseStatusCode, errors_from_validation_error, Response


def create_product_handler(body: dict) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=ResponseStatusCode.BAD_REQUEST
        )
    try:
        data = ProductCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
        
    try:
        with get_db() as db:
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
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_product_handler(product_id: str) -> Response:
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
            return error(
                message="Invalid product_id",
                status_code=ResponseStatusCode.BAD_REQUEST,
                details=errors_from_validation_error(e)
            )
    
    try:
        with get_db() as db:
            product = get_product(db, product_id)

            if not product:
                return error(
                    message="Product not found",
                    status_code=ResponseStatusCode.NOT_FOUND
                )
            
            response = ProductResponse.model_validate(product)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_all_products_handler() -> Response:
    try:
        with get_db() as db:
            products = get_all_products(db)
            return success([
                ProductResponse.model_validate(product) for product in products
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def update_product_handler(product_id: str, body: dict | None) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=ResponseStatusCode.BAD_REQUEST
        )
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid product_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    try:
        data = ProductUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        with get_db() as db:
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
                    status_code=ResponseStatusCode.NOT_FOUND
                )
            
            response = ProductResponse.model_validate(product)
            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def delete_product_handler(product_id: str) -> Response:
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid product_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    try:
        with get_db() as db:
            deleted_id = delete_product(db, product_id)

            if not deleted_id:
                return error(
                    message="Product not found",
                    status_code=ResponseStatusCode.NOT_FOUND
                )

            return success(
                data={"product_id": str(deleted_id)}
            )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def search_products_handler(query: str) -> Response:
    if not query or not query.strip():
        return error(
            message="Query parameter is required and cannot be empty",
            status_code=ResponseStatusCode.BAD_REQUEST
        )

    try:   
        with get_db() as db:
            products = search_products_by_name(db, query)

            return success([
                ProductResponse.model_validate(product) for product in products
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )
