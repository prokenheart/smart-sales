from pydantic import Field, ConfigDict, field_validator
import uuid
from datetime import datetime
from decimal import Decimal
from datetime import date
from app.schemas.base_schema import CamelCaseModel


class PriceBase(CamelCaseModel):
    product_id: uuid.UUID
    price_amount: Decimal = Field(gt=0)
    price_date: date


class PriceCreate(PriceBase):
    @field_validator("price_date")
    @classmethod
    def validate_price_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Price_date must be today or in the future")
        return v


class PriceIdPath(CamelCaseModel):
    price_id: uuid.UUID


class PriceResponse(PriceBase):
    price_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PriceUpdate(CamelCaseModel):
    product_id: uuid.UUID | None = None
    price_amount: Decimal | None = Field(default=None, gt=0)
    price_date: date | None = None

    @field_validator("price_date")
    @classmethod
    def validate_price_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Price_date must be today or in the future")
        return v
