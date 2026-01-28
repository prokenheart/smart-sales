from app.logger import logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from app.routes.customer import router as customer_router
from app.routes.product import router as product_router
from app.routes.price import router as price_router
from app.routes.status import router as status_router
from app.routes.user import router as user_router
from app.routes.order import router as order_router
from app.routes.item import router as item_router

app = APIGatewayRestResolver(
    debug=True
)

# include routers
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(price_router)
app.include_router(status_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(item_router)

@logger.inject_lambda_context
def lambda_handler(event, context):
    # logger.info("DEBUG_EVENT_PATH", extra={
    #     "path": event.get("path"),
    #     "rawPath": event.get("rawPath"),
    #     "resource": event.get("resource"),
    #     "requestContext": event.get("requestContext"),
    # })
    return app.resolve(event, context)
