from pydantic import ValidationError
from app.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderIdPath,
    OrderResponse,
    OrderUpdateStatus,
    OrderDateQuery
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
    NotFoundError
)

from app.core.response import success, error

def create_order_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        data = OrderCreate.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
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
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError:
            return error(
                message="Invalid order_id",
                status_code=400
            )
    
    try:
        with get_db() as db:
            order = get_order(db, order_id)
            if not order:
                return error(
                    message="Order not found",
                    status_code=404
                )
            
            response = OrderResponse.model_validate(order)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
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
            status_code=500,
            details=str(e)
        )

def get_orders_by_user_handler(user_id: str):
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid user_id",
            status_code=400,
            details=e.errors()
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
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_orders_by_customer_handler(customer_id: str):
    try:
        customer_id = UserIdPath.model_validate({"user_id": customer_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=400,
            details=e.errors()
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
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_orders_by_status_handler(status_code: str):
    try:
        status_code = StatusCode.model_validate({"status_code": status_code}).status_code
    except ValidationError as e:
        safe_errors = []
        for err in e.errors():
            safe_err = {k: v for k, v in err.items() if k != 'ctx'}  # loại bỏ 'ctx' chứa ValueError
            safe_errors.append(safe_err)
        
        return error(
            message="Invalid status code",
            status_code=400,
            details=safe_errors
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
            status_code=404
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
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
            status_code=400,
            details=str(e)
        )
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def update_order_status_handler(order_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = OrderUpdateStatus.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
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
                    status_code=404
                )
            
            response = OrderResponse.model_validate(order)
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

def delete_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        with get_db() as db:
            deleted_id = delete_order(db, order_id)

            if not deleted_id:
                return error(
                    message="Order not found",
                    status_code=404
                )

            return success(
                data={"order_id": str(deleted_id)}
            )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )