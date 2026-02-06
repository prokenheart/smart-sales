from aws_lambda_powertools.event_handler.router import Router
from app.handlers.item import (
    get_item_handler,
    get_all_items_handler,
    get_items_by_order_handler,
    update_item_handler,
)

router = Router()


@router.get("/orders/<order_id>/items/<product_id>")
def get_item(order_id: str, product_id: str):
    return get_item_handler(order_id, product_id)


@router.get("/items")
def get_all_items():
    return get_all_items_handler()


@router.get("/orders/<order_id>/items")
def get_items_by_order(order_id: str):
    return get_items_by_order_handler(order_id)


@router.put("/orders/<order_id>/items")
def update_item(order_id: str):
    body = router.current_event.json_body
    return update_item_handler(order_id, body)
