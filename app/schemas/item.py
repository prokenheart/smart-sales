from pydantic import BaseModel
import uuid
from datetime import datetime
import decimal

class ItemBase(BaseModel):
    product_id: uuid.UUID
    item_quantity: int

class ItemList(BaseModel):
    list_item: list[ItemBase]

class ItemResponse(ItemBase):
    item_price: decimal.Decimal
    order_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True