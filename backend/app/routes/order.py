from aws_lambda_powertools.event_handler.router import Router
from app.handlers.order import (
    create_order_handler,
    get_order_handler,
    get_orders_handler,
    update_order_status_handler,
    delete_order_handler,
    create_order_attachment_upload_url_handler,
    create_order_attachment_get_url_handler,
    delete_order_attachment_handler,
    confirm_order_attachment_handler,
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
def get_orders():
    params = router.current_event.query_string_parameters or {}
    return get_orders_handler(params)


@router.patch("/orders/<order_id>")
def update_order(order_id: str):
    body = router.current_event.json_body
    return update_order_status_handler(order_id, body)


@router.delete("/orders/<order_id>")
def delete_order(order_id: str):
    return delete_order_handler(order_id)


@router.post("/orders/<order_id>/attachment/upload-url")
def upload_file(order_id: str):
    body = router.current_event.json_body
    return create_order_attachment_upload_url_handler(order_id, body)


@router.post("/orders/<order_id>/attachment/view-url")
def get_file_url(order_id: str):
    return create_order_attachment_get_url_handler(order_id)


@router.delete("/orders/<order_id>/attachment")
def delete_file(order_id: str):
    return delete_order_attachment_handler(order_id)


@router.put("/orders/<order_id>/attachment")
def confirm_attachment(order_id: str):
    body = router.current_event.json_body
    return confirm_order_attachment_handler(order_id, body)
