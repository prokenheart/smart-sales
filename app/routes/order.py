from aws_lambda_powertools.event_handler.router import Router
from app.handlers.order import (
    create_order_handler,
    get_order_handler,
    get_all_orders_handler,
    get_orders_by_user_handler,
    get_orders_by_customer_handler,
    get_orders_by_status_handler,
    get_orders_by_date_handler,
    update_order_status_handler,
    delete_order_handler
)
router = Router()

@router.post("/orders")
def create_order():
    body = router.current_event.json_body
    return create_order_handler(body)

@router.get("/orders/<order_id>")
def get_order(order_id: str):
    return get_order_handler(order_id)

@router.get("/orders")
def get_all_orders():
    params = router.current_event.query_string_parameters or {}

    if "user_id" in params:
        return get_orders_by_user_handler(params["user_id"])
    
    if "customer_id" in params:
        return get_orders_by_customer_handler(params["customer_id"])
    
    if "status_code" in params:
        return get_orders_by_status_handler(params["status_code"])
    
    if "order_date" in params:
        return get_orders_by_date_handler(params["order_date"])

    return get_all_orders_handler()

@router.patch("/orders/<order_id>")
def update_order(order_id: str):
    body = router.current_event.json_body
    return update_order_status_handler(order_id, body)

@router.delete("/orders/<order_id>")
def delete_order(order_id: str):
    return delete_order_handler(order_id)