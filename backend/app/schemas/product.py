from pydantic import Field, ConfigDict
import uuid
from datetime import datetime
from app.schemas.base_schema import CamelCaseModel


class ProductBase(CamelCaseModel):
    product_name: str
    product_description: str | None = None
    product_quantity: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductIdPath(CamelCaseModel):
    product_id: uuid.UUID


class ProductResponse(ProductBase):
    product_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(CamelCaseModel):
    product_name: str | None = None
    product_description: str | None = None
    product_quantity: int | None = Field(default=None, ge=0)
