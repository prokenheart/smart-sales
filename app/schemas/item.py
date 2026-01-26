from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime
from decimal import Decimal

class ItemBase(BaseModel):
    product_id: uuid.UUID
    item_quantity: int = Field(gt=0)

class ItemCreate(ItemBase):
    pass

class ItemList(BaseModel):
    list_item: list[ItemCreate]

class ItemResponse(ItemBase):
    item_price: Decimal
    order_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)