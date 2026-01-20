from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    product_quantity: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_quantity: Optional[int] = None