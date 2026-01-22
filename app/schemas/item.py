from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from decimal import Decimal

class ItemBase(BaseModel):
    product_id: uuid.UUID
    item_quantity: int = Field(gt=0)

class ItemList(BaseModel):
    list_item: list[ItemBase]

class ItemResponse(ItemBase):
    item_price: Decimal
    order_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True