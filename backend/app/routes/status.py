from aws_lambda_powertools.event_handler.router import Router
from app.handlers.status import (
    get_status_handler,
    get_status_by_code_handler,
    get_all_statuses_handler,
)

router = Router()


@router.get("/statuses/<status_id>")
def get_status(status_id: str):
    return get_status_handler(status_id)


@router.get("/statuses")
def get_all_statuses():
    params = router.current_event.query_string_parameters or {}

    if "code" in params:
        return get_status_by_code_handler(params["code"])

    return get_all_statuses_handler()
