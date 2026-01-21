from logger import logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from routes.customer import router as customer_router
from routes.product import router as product_router
from routes.price import router as price_router
from routes.status import router as status_router

app = APIGatewayRestResolver(
    debug=True
)

# include routers
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(price_router)
app.include_router(status_router)

@logger.inject_lambda_context
def lambda_handler(event, context):
    # logger.info("DEBUG_EVENT_PATH", extra={
    #     "path": event.get("path"),
    #     "rawPath": event.get("rawPath"),
    #     "resource": event.get("resource"),
    #     "requestContext": event.get("requestContext"),
    # })
    return app.resolve(event, context)
