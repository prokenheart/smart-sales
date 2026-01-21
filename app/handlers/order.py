from pydantic import ValidationError
from database import SessionLocal
from logger import logger
from schemas.order import (
    OrderCreate,
    OrderIdPath,
    OrderResponse,
    OrderUpdateStatus,
    OrderDateQuery
)

from schemas.user import UserIdPath

from services.order import (
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

from core.response import success, error

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
        
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def get_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError:
            return error(
                message="Invalid order_id",
                status_code=400
            )
    
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def get_all_orders_handler():
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def get_orders_by_user_handler(user_id: str):
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid user_id",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def get_orders_by_customer_handler(customer_id: str):
    try:
        customer_id = UserIdPath.model_validate({"user_id": customer_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid customer_id",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def get_orders_by_status_handler(status_id: str):
    try:
        status_id = OrderIdPath.model_validate({"order_id": status_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid status_id",
            status_code=400,
            details=e.errors()
        )
        
    db = SessionLocal()
    try:
        orders = get_orders_by_status(db, status_id)
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

    finally:
        db.close()

def get_orders_by_date_handler(date_str: str):
    db = SessionLocal()
    try:
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

    finally:
        db.close()

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
    
    db = SessionLocal()
    try:
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

    finally:
        db.close()

def delete_order_handler(order_id: str):
    try:
        order_id = OrderIdPath.model_validate({"order_id": order_id}).order_id
    except ValidationError as e:
        return error(
            message="Invalid order_id",
            status_code=400,
            details=e.errors()
        )
    
    db = SessionLocal()
    try:
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

    finally:
        db.close()