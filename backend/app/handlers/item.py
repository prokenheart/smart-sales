from pydantic import ValidationError
from http import HTTPStatus
from app.database import get_db
from app.schemas.item import ItemResponse, ItemList
from app.models.order import WrongStatus
from app.schemas.product import ProductIdPath
from app.schemas.order import OrderIdPath

from app.services.item import (
    get_item,
    get_items_by_order,
    get_all_items,
    update_list_of_item,
    NotFoundError,
    NotEnoughError,
)

from app.core.response import (
    success,
    error,
    errors_from_validation_error,
    Response,
)


def get_item_handler(order_id: str, product_id: str) -> Response:
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
        product_id = ProductIdPath.model_validate({"product_id": product_id}).product_id
    except ValidationError as e:
        return error(
            message="Invalid id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            item = get_item(db, order_id, product_id)
            if not item:
                return error(
                    message="Item not found", status_code=HTTPStatus.NOT_FOUND
                )

            response = ItemResponse.model_validate(item)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_all_items_handler() -> Response:
    try:
        with get_db() as db:
            items = get_all_items(db)
            return success([ItemResponse.model_validate(item) for item in items])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_items_by_order_handler(order_id: str) -> Response:
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            items = get_items_by_order(db, order_id)
            return success([ItemResponse.model_validate(item) for item in items])

    except NotFoundError as e:
        return error(message=str(e), status_code=HTTPStatus.NOT_FOUND)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def update_item_handler(order_id: str, body: dict) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=HTTPStatus.BAD_REQUEST,
        )
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        data = ItemList.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            items = update_list_of_item(db, order_id, data.list_item)

            return success([ItemResponse.model_validate(item) for item in items])

    except NotFoundError as e:
        return error(message=str(e), status_code=HTTPStatus.NOT_FOUND)

    except ValueError as e:
        return error(
            message=str(e), status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    except NotEnoughError as e:
        return error(
            message=str(e), status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    except WrongStatus as e:
        return error(
            message=str(e), status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )
