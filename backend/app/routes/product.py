from aws_lambda_powertools.event_handler.router import Router
from app.handlers.product import (
    create_product_handler,
    get_product_handler,
    get_all_products_handler,
    search_products_handler,
    update_product_handler,
    delete_product_handler,
)

router = Router()


@router.post("/products")
def create_product():
    body = router.current_event.json_body
    return create_product_handler(body)


@router.get("/products/<product_id>")
def get_product(product_id: str):
    return get_product_handler(product_id)


@router.get("/products")
def get_all_products():
    params = router.current_event.query_string_parameters or {}

    if "query" in params:
        return search_products_handler(params["query"])

    return get_all_products_handler()


@router.put("/products/<product_id>")
def update_product(product_id: str):
    body = router.current_event.json_body
    return update_product_handler(product_id, body)


@router.delete("/products/<product_id>")
def delete_product(product_id: str):
    return delete_product_handler(product_id)
