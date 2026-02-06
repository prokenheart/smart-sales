from pydantic import ValidationError
from app.database import get_db
from app.schemas.price import PriceCreate, PriceIdPath, PriceResponse, PriceUpdate

from app.schemas.product import ProductIdPath

from app.services.price import (
    create_price,
    get_price,
    get_prices_by_product,
    get_all_prices,
    update_price,
    delete_price,
    NotFoundError,
)

from app.core.response import (
    success,
    error,
    ResponseStatusCode,
    errors_from_validation_error,
    Response,
)


def create_price_handler(body: dict | None) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=ResponseStatusCode.BAD_REQUEST,
        )
    try:
        data = PriceCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            price = create_price(
                db, data.product_id, data.price_amount, data.price_date
            )

            response = PriceResponse.model_validate(price)
            return success(data=response, status_code=201)

    except NotFoundError as e:
        return error(message=str(e), status_code=ResponseStatusCode.NOT_FOUND)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_price_handler(price_id: str) -> Response:
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError as e:
        return error(
            message="Invalid price_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            price = get_price(db, price_id)
            if not price:
                return error(
                    message="Price not found", status_code=ResponseStatusCode.NOT_FOUND
                )

            response = PriceResponse.model_validate(price)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_all_prices_handler() -> Response:
    try:
        with get_db() as db:
            prices = get_all_prices(db)
            return success([PriceResponse.model_validate(price) for price in prices])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_prices_by_product_handler(product_id: str) -> Response:
    try:
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid product_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            prices = get_prices_by_product(db, product_id)
            return success([PriceResponse.model_validate(price) for price in prices])

    except NotFoundError as e:
        return error(message=str(e), status_code=ResponseStatusCode.NOT_FOUND)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def update_price_handler(price_id: str, body: dict | None) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=ResponseStatusCode.BAD_REQUEST,
        )
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError as e:
        return error(
            message="Invalid price_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        data = PriceUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            price = update_price(
                db, price_id, data.product_id, data.price_amount, data.price_date
            )

            response = PriceResponse.model_validate(price)
            return success(response)

    except NotFoundError as e:
        return error(message=str(e), status_code=ResponseStatusCode.NOT_FOUND)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def delete_price_handler(price_id: str) -> Response:
    try:
        price_id = PriceIdPath.model_validate({"price_id": price_id}).price_id
    except ValidationError as e:
        return error(
            message="Invalid price_id",
            status_code=ResponseStatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            deleted_id = delete_price(db, price_id)

            if not deleted_id:
                return error(
                    message="Price not found", status_code=ResponseStatusCode.NOT_FOUND
                )

            return success(data={"price_id": str(deleted_id)})

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR,
            details=str(e),
        )
