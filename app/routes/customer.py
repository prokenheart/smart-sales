from aws_lambda_powertools.event_handler.router import Router
from logger import logger
from handlers.customer import (
    create_customer_handler,
    get_customer_handler,
    get_all_customers_handler,
    get_customer_by_email_handler,
    search_customers_handler,
    update_customer_handler,
    delete_customer_handler
)
router = Router()

@router.post("/customers")
def create_customer():
    body = router.current_event.json_body
    return create_customer_handler(body)

@router.get("/customers/<customer_id>")
def get_customer(customer_id: str):
    return get_customer_handler(customer_id)

@router.get("/customers")
def get_all_customers():
    params = router.current_event.query_string_parameters or {}

    if "email" in params:
        return get_customer_by_email_handler(params["email"])

    if "query" in params:
        return search_customers_handler(params["query"])

    return get_all_customers_handler()

@router.put("/customers/<customer_id>")
def update_customer(customer_id: str):
    body = router.current_event.json_body
    return update_customer_handler(customer_id, body)

@router.delete("/customers/<customer_id>")
def delete_customer(customer_id: str):
    return delete_customer_handler(customer_id)