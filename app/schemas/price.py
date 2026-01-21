from pydantic import BaseModel
import uuid
from datetime import datetime
import decimal
from datetime import date

class PriceBase(BaseModel):
    product_id: uuid.UUID
    price_amount: decimal.Decimal
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
    price_amount: decimal.Decimal | None = None
    price_date: date | None = None