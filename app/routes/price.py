from aws_lambda_powertools.event_handler.router import Router
from app.handlers.price import (
    create_price_handler,
    get_price_handler,
    get_all_prices_handler,
    get_prices_by_product_handler,
    update_price_handler,
    delete_price_handler
)
router = Router()

@router.post("/prices")
def create_price():
    body = router.current_event.json_body
    return create_price_handler(body)

@router.get("/prices/<price_id>")
def get_price(price_id: str):
    return get_price_handler(price_id)

@router.get("/prices")
def get_all_prices():
    params = router.current_event.query_string_parameters or {}

    if "product_id" in params:
        return get_prices_by_product_handler(params["product_id"])

    return get_all_prices_handler()

@router.put("/prices/<price_id>")
def update_price(price_id: str):
    body = router.current_event.json_body
    return update_price_handler(price_id, body)

@router.delete("/prices/<price_id>")
def delete_price(price_id: str):
    return delete_price_handler(price_id)