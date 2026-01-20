from aws_lambda_powertools import Logger

logger = Logger(
    service="my_service",
    level="INFO"
)
