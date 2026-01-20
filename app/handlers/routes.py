from handlers.customer import *
from handlers.status import *
from handlers.product import *
from handlers.price import *

CUSTOMER_HANDLERS = {
    "collection": {
        "POST": create_customer_handler,
        "GET": get_customers_collection_handler,
    },
    "item": {
        "GET": get_customer_handler,
        "PUT": update_customer_handler,
        "DELETE": delete_customer_handler,
    },
}

STATUS_HANDLERS = {
    "collection": {
        "POST": create_status_handler,
        "GET": get_all_statuss_handler,
    },
    "item": {
        "GET": get_status_handler,
        "PUT": update_status_handler,
        "DELETE": delete_status_handler,
    },
}

PRODUCT_HANDLERS = {
    "collection": {
        "POST": create_product_handler,
        "GET": get_all_products_handler,
    },
    "item": {
        "GET": get_product_handler,
        "PUT": update_product_handler,
        "DELETE": delete_product_handler,
    },
}

PRICE_HANDLERS = {
    "collection": {
        "POST": create_price_handler,
        "GET": get_prices_collection_handler,
    },
    "item": {
        "GET": get_price_handler,
        "PUT": update_price_handler,
        "DELETE": delete_price_handler,
    },
}
