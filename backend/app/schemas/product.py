from pydantic import Field, ConfigDict
import uuid
from datetime import datetime
from app.schemas.base_schema import CamelCaseModel
from decimal import Decimal


class ProductBase(CamelCaseModel):
    product_name: str
    product_description: str | None = None
    product_quantity: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductIdPath(CamelCaseModel):
    product_id: uuid.UUID


class PriceResponse(CamelCaseModel):
    price_id: uuid.UUID
    price_amount: Decimal | None = Field(default=None, gt=0)

    model_config = ConfigDict(from_attributes=True)

class ProductResponse(ProductBase):
    product_id: uuid.UUID
    updated_at: datetime
    prices: list[PriceResponse]

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(CamelCaseModel):
    product_name: str | None = None
    product_description: str | None = None
    product_quantity: int | None = Field(default=None, ge=0)
