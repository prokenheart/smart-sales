from pydantic import ValidationError
import re
from enum import Enum
from http import HTTPStatus
from app.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerIdPath,
    CustomerEmailQuery,
    CustomerResponse,
    CustomerUpdate,
)

from app.services.customer import (
    create_customer,
    get_customer,
    get_all_customers,
    get_customer_by_email,
    update_customer,
    delete_customer,
    search_customers_by_email,
    search_customers_by_phone,
    search_customers_by_name,
    DuplicateEmailError,
)

from app.core.response import (
    success,
    error,
    errors_from_validation_error,
    Response,
)


class SearchType(str, Enum):
    EMAIL = "email"
    NAME = "name"
    PHONE = "phone"


PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")
UPPERCASE_REGEX = re.compile(r"[A-Z]")


def create_customer_handler(body: dict | None) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=HTTPStatus.BAD_REQUEST,
        )
    try:
        data = CustomerCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            customer = create_customer(
                db, data.customer_name, data.customer_email, data.customer_phone
            )
            response = CustomerResponse.model_validate(customer)
            return success(data=response, status_code=HTTPStatus.CREATED)

    except DuplicateEmailError as e:
        return error(message=str(e), status_code=HTTPStatus.CONFLICT)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_customer_handler(customer_id: str) -> Response:
    try:
        customer_id = CustomerIdPath.model_validate(
            {"customer_id": customer_id}
        ).customer_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            customer = get_customer(db, customer_id)

            if not customer:
                return error(
                    message="Customer not found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

            response = CustomerResponse.model_validate(customer)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_all_customers_handler() -> Response:
    try:
        with get_db() as db:
            customers = get_all_customers(db)
            return success(
                [CustomerResponse.model_validate(customer) for customer in customers]
            )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def get_customer_by_email_handler(customer_email: str) -> Response:
    try:
        customer_email = CustomerEmailQuery.model_validate(
            {"customer_email": customer_email}
        ).customer_email
    except ValidationError as e:
        return error(
            message="Invalid email parameter",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            customer = get_customer_by_email(db, customer_email)

            if not customer:
                return error(
                    message="Customer not found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

            response = CustomerResponse.model_validate(customer)
            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def update_customer_handler(customer_id: str, body: dict | None) -> Response:
    if body is None:
        return error(
            message="Request body is required",
            status_code=HTTPStatus.BAD_REQUEST,
        )
    try:
        customer_id = CustomerIdPath.model_validate(
            {"customer_id": customer_id}
        ).customer_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        data = CustomerUpdate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            customer = update_customer(
                db,
                customer_id,
                data.customer_name,
                data.customer_email,
                data.customer_phone,
            )

            if not customer:
                return error(
                    message="Customer not found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

            response = CustomerResponse.model_validate(customer)
            return success(response)

    except DuplicateEmailError as e:
        return error(message=str(e), status_code=HTTPStatus.CONFLICT)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def delete_customer_handler(customer_id: str) -> Response:
    try:
        customer_id = CustomerIdPath.model_validate(
            {"customer_id": customer_id}
        ).customer_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=HTTPStatus.BAD_REQUEST,
            details=errors_from_validation_error(e),
        )

    try:
        with get_db() as db:
            deleted_id = delete_customer(db, customer_id)

            if not deleted_id:
                return error(
                    message="Customer not found",
                    status_code=HTTPStatus.NOT_FOUND,
                )

            return success(data={"customer_id": str(deleted_id)})

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def search_customers_handler(query: str) -> Response:
    if not query or not query.strip():
        return error(
            message="Query parameter is required and cannot be empty",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    try:
        with get_db() as db:
            keyword = query.strip()
            search_type = detect_search_type(keyword)

            if search_type == SearchType.EMAIL:
                customers = search_customers_by_email(db, keyword)
            elif search_type == SearchType.PHONE:
                customers = search_customers_by_phone(db, keyword)
            else:
                customers = search_customers_by_name(db, keyword)

            return success(
                [CustomerResponse.model_validate(customer) for customer in customers]
            )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=str(e),
        )


def detect_search_type(keyword: str) -> str:
    keyword = keyword.strip()
    if "@" in keyword:
        return SearchType.EMAIL
    if PHONE_REGEX.search(keyword):
        return SearchType.PHONE
    if UPPERCASE_REGEX.search(keyword) or " " in keyword:
        return SearchType.NAME
    return SearchType.EMAIL
