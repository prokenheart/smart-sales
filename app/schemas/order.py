from pydantic import BaseModel
import uuid
from datetime import datetime
from decimal import Decimal

class OrderBase(BaseModel):
    customer_id: uuid.UUID
    user_id: uuid.UUID

class OrderCreate(OrderBase):
    pass

class OrderIdPath(BaseModel):
    order_id: uuid.UUID

class OrderResponse(OrderBase):
    order_id: uuid.UUID
    order_total: Decimal
    status_id: uuid.UUID
    order_date: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderUpdateStatus(BaseModel):
    status_id: uuid.UUID

class OrderDateQuery(BaseModel):
    order_date: datetime