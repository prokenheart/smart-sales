from pydantic import BaseModel
import uuid
from datetime import datetime

class ProductBase(BaseModel):
    product_name: str
    product_description: str | None = None
    product_quantity: int

class ProductCreate(ProductBase):
    pass

class ProductIdPath(BaseModel):
    product_id: uuid.UUID

class ProductResponse(ProductBase):
    product_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    product_name: str | None = None
    product_description: str | None = None
    product_quantity: int | None = None