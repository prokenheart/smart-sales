from pydantic import BaseModel, Field, ConfigDict, field_validator
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

    model_config = ConfigDict(from_attributes=True)

class OrderUpdateStatus(BaseModel):
    status_id: uuid.UUID

class OrderDateQuery(BaseModel):
    order_date: datetime

class OrderAttachmentResponse(BaseModel):
    order_id: uuid.UUID
    order_attachment: str

    model_config = ConfigDict(from_attributes=True)

class OrderAttachmentUploadURLRequest(BaseModel):
    content_type: str = Field(..., alias="contentType")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        allowed = {
            "image/png",
            "image/jpeg",
            "application/pdf"
        }
        if v not in allowed:
            raise ValueError("Unsupported content type")
        return v