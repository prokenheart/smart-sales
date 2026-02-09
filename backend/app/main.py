from app.core.logger import logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.metrics import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools import Tracer


from app.routes.customer import router as customer_router
from app.routes.product import router as product_router
from app.routes.price import router as price_router
from app.routes.status import router as status_router
from app.routes.user import router as user_router
from app.routes.order import router as order_router
from app.routes.item import router as item_router

SERVICE_NAME = "SmartSalesApi"

app = APIGatewayRestResolver(debug=True)
tracer = Tracer(service=SERVICE_NAME)
metrics = Metrics(namespace="MyApplication", service=SERVICE_NAME)

# include routers
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(price_router)
app.include_router(status_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(item_router)


@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    metrics.add_dimension(name="Path", value="/orders")
    metrics.add_metric(name="ApiRequest", unit=MetricUnit.Count, value=1)

    return app.resolve(event, context)
