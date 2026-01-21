from aws_lambda_powertools.event_handler.router import Router
from logger import logger
from handlers.user import (
    create_user_handler,
    get_user_handler,
    get_all_users_handler,
    get_user_by_account_handler,
    get_user_by_email_handler,
    search_users_handler,
    update_user_info_handler,
    update_user_password_handler,
    delete_user_handler
)
router = Router()

@router.post("/users")
def create_user():
    body = router.current_event.json_body
    return create_user_handler(body)

@router.get("/users/<user_id>")
def get_user(user_id: str):
    return get_user_handler(user_id)

@router.get("/users")
def get_all_users():
    params = router.current_event.query_string_parameters or {}

    if "account" in params:
        return get_user_by_account_handler(params["account"])

    if "email" in params:
        return get_user_by_email_handler(params["email"])

    if "query" in params:
        return search_users_handler(params["query"])

    return get_all_users_handler()

@router.patch("/users/<user_id>")
def update_user_info(user_id: str):
    body = router.current_event.json_body
    return update_user_info_handler(user_id, body)

@router.patch("/users/<user_id>/password")
def update_user_password(user_id: str):
    body = router.current_event.json_body
    return update_user_password_handler(user_id, body)    

@router.delete("/users/<user_id>")
def delete_user(user_id: str):
    return delete_user_handler(user_id)