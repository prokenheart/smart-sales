from aws_lambda_powertools.event_handler.router import Router
from logger import logger
from handlers.status import (
    create_status_handler,
    get_status_handler,
    get_all_statuses_handler,
    update_status_handler,
    delete_status_handler
)
router = Router()

@router.post("/statuses")
def create_status():
    body = router.current_event.json_body
    return create_status_handler(body)

@router.get("/statuses/<status_id>")
def get_status(status_id: str):
    return get_status_handler(status_id)

@router.get("/statuses")
def get_all_statuses():
    return get_all_statuses_handler()

@router.put("/statuses/<status_id>")
def update_status(status_id: str):
    body = router.current_event.json_body
    return update_status_handler(status_id, body)

@router.delete("/statuses/<status_id>")
def delete_status(status_id: str):
    return delete_status_handler(status_id)