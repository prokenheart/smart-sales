from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

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
    customer_name: str | None = None
    customer_email: EmailStr | None = None
    customer_phone: str | None = None