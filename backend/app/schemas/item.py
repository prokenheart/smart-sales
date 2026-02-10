from pydantic import Field, ConfigDict
import uuid
from datetime import datetime
from decimal import Decimal
from app.schemas.base_schema import CamelCaseModel


class ItemBase(CamelCaseModel):
    product_id: uuid.UUID
    item_quantity: int = Field(gt=0)


class ItemCreate(ItemBase):
    pass


class ItemList(CamelCaseModel):
    list_item: list[ItemCreate]


class ItemResponse(ItemBase):
    item_price: Decimal
    order_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
