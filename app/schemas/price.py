from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional
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
    product_id: Optional[uuid.UUID] = None
    price_amount: Optional[decimal.Decimal] = None
    price_date: Optional[date] = None