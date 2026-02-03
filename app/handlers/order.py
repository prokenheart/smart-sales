from pydantic import ValidationError
from app.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderIdPath,
    OrderResponse,
    OrderUpdateStatus,
    OrderDateQuery,
    OrderAttachmentResponse,
    OrderAttachmentUploadURLRequest
)

from app.schemas.user import UserIdPath
from app.schemas.status import StatusCode

from app.services.order import (
    create_order,
    get_order,
    get_orders_by_user,
    get_orders_by_customer,
    get_orders_by_status,
    get_orders_by_date,
    get_all_orders,
    update_order_status,
    delete_order,
    update_order_attachment_url,
    NotFoundError
)

from app.s3_client import generate_presigned_upload_url, generate_presigned_get_url, delete_file_from_s3

from app.core.response import success, error, StatusCode, errors_from_validation_error

def create_order_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=StatusCode.BAD_REQUEST
        )
    try:
        data = OrderCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
        
    try:
        with get_db() as db:
            order = create_order(
                db,
                data.customer_id,
                data.user_id
            )

            response = OrderResponse.model_validate(order)
            return success(
                data=response,
                status_code=201
            )
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=StatusCode.NOT_FOUND
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
            return error(
                message="Invalid order_id",
                status_code=StatusCode.BAD_REQUEST,
                details=errors_from_validation_error(e)
            )
    
    try:
        with get_db() as db:
            order = get_order(db, order_id)
            if not order:
                return error(
                    message="Order not found",
                    status_code=StatusCode.NOT_FOUND
                )
            
            response = OrderResponse.model_validate(order)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )
    
def get_all_orders_handler():
    try:
        with get_db() as db:
            orders = get_all_orders(db)
            return success([
                OrderResponse.model_validate(order) for order in orders
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_orders_by_user_handler(user_id: str):
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid user_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
        
    try:
        with get_db() as db:
            orders = get_orders_by_user(db, user_id)
            return success([
                OrderResponse.model_validate(order) for order in orders
            ])
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=StatusCode.NOT_FOUND
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_orders_by_customer_handler(customer_id: str):
    try:
        customer_id = UserIdPath.model_validate({"user_id": customer_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
        
    try:
        with get_db() as db:
            orders = get_orders_by_customer(db, customer_id)
            return success([
                OrderResponse.model_validate(order) for order in orders
            ])
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=StatusCode.NOT_FOUND
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_orders_by_status_handler(status_code: str):
    try:
        status_code = StatusCode.model_validate({"status_code": status_code}).status_code
    except ValidationError as e:
        return error(
            message="Invalid status code",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
        
    try:
        with get_db() as db:
            orders = get_orders_by_status(db, status_code)
            return success([
                OrderResponse.model_validate(order) for order in orders
            ])
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=StatusCode.NOT_FOUND
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def get_orders_by_date_handler(date_str: str):
    try:
        with get_db() as db:
            date_query = OrderDateQuery.model_validate({"order_date": date_str}).order_date
            orders = get_orders_by_date(db, date_query)
            return success([
                OrderResponse.model_validate(order) for order in orders
            ])
    
    except ValidationError as e:
        return error(
            message="Invalid date format",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def update_order_status_handler(order_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=StatusCode.BAD_REQUEST
        )
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    try:
        data = OrderUpdateStatus.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        with get_db() as db:
            order = update_order_status(
                db,
                order_id,
                data.status_id
            )

            if not order:
                return error(
                    message="Order not found",
                    status_code=StatusCode.NOT_FOUND
                )
            
            response = OrderResponse.model_validate(order)
            return success(response)
    
    except NotFoundError as e:
        return error(
            message=str(e),
            status_code=StatusCode.NOT_FOUND
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def delete_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    try:
        with get_db() as db:
            deleted_id = delete_order(db, order_id)

            if not deleted_id:
                return error(
                    message="Order not found",
                    status_code=StatusCode.NOT_FOUND
                )

            return success(
                data={"order_id": str(deleted_id)}
            )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )
    
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def create_order_attachment_upload_url_handler(order_id: str, body):
    if body is None:
        return error(
            message="Request body is required",
            status_code=StatusCode.BAD_REQUEST
        )

    try:
        data = OrderAttachmentUploadURLRequest.model_validate(body)
        content_type = data.content_type
    except ValidationError as e:
        return error(
            message="Invalid content type",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        upload_url, s3_key = generate_presigned_upload_url(
            content_type=content_type,
            expires_in=300
        )

        response = {
            "upload_url": upload_url,
            "s3_key": s3_key,
            "max_file_size": MAX_FILE_SIZE
        }
        return success(response)
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )

def confirm_order_attachment_handler(order_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=StatusCode.BAD_REQUEST
        )

    s3_key = body.get("s3_key")
    if not s3_key:
        return error("s3_key is required", 400)

    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id", 
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )

    try:
        with get_db() as db:
            order = update_order_attachment_url(
                db=db,
                order_id=order_id,
                attachment_url=s3_key
            )

        response = OrderAttachmentResponse.model_validate(order)
        return success(response)

    except NotFoundError as e:
        return error(str(e), 404)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )
    
def create_order_attachment_get_url_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    with get_db() as db:
        order = get_order(db, order_id)
        if not order:
            return error(
                message="Order not found",
                status_code=StatusCode.NOT_FOUND
            )
        
        if order.order_attachment is None:
            return error(
                message="No attachment found for this order",
                status_code=StatusCode.NOT_FOUND
            )
        s3_key = order.order_attachment


    try:
        get_url = generate_presigned_get_url(
            key=s3_key,
            expires_in=300
        )

        response = {
            "get_url": get_url
        }
        return success(response)
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )
    
def delete_order_attachment_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=StatusCode.BAD_REQUEST,
            details=errors_from_validation_error(e)
        )
    
    try:
        with get_db() as db:
            order = get_order(db, order_id)
            if not order:
                return error(
                    message="Order not found",
                    status_code=StatusCode.NOT_FOUND
                )
            
            if order.order_attachment is None:
                return error(
                    message="No attachment found for this order",
                    status_code=StatusCode.NOT_FOUND
                )
            s3_key = order.order_attachment

            delete_file_from_s3(s3_key)

            update_order_attachment_url(
                db=db,
                order_id=order_id,
                attachment_url=None
            )

            response = {
                "message": "Attachment deleted successfully"
            }

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
            details=str(e)
        )