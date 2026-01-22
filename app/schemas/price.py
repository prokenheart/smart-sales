from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from decimal import Decimal
from datetime import date

class PriceBase(BaseModel):
    product_id: uuid.UUID
    price_amount: Decimal = Field(gt=0)
    price_date: date

class PriceCreate(PriceBase):
    pass

class PriceIdPath(BaseModel):
    price_id: uuid.UUID

class PriceResponse(PriceBase):
    price_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class PriceUpdate(BaseModel):
    product_id: uuid.UUID | None = None
    price_amount: Decimal | None = Field(default=None, gt=0)
    price_date: date | None = None