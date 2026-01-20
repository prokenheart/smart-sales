from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime
from typing import Optional

class CustomerBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerIdPath(BaseModel):
    customer_id: uuid.UUID

class CustomerEmailQuery(BaseModel):
    customer_email: EmailStr

class CustomerResponse(CustomerBase):
    customer_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None