from pydantic import BaseModel, Field, ConfigDict, field_validator
import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Literal
from app.schemas.status import StatusCode


class OrderBase(BaseModel):
    customer_id: uuid.UUID
    user_id: uuid.UUID


class OrderCreate(OrderBase):
    pass


class OrderIdPath(BaseModel):
    order_id: uuid.UUID


class StatusResponse(BaseModel):
    status_code: str

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(OrderBase):
    order_id: uuid.UUID
    order_total: Decimal
    status_id: uuid.UUID
    status: StatusResponse
    order_date: datetime
    order_attachment: str | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderUpdateStatus(StatusCode):
    pass

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
        allowed = {"image/png", "image/jpeg", "application/pdf"}
        if v not in allowed:
            raise ValueError("Unsupported content type")
        return v


class OrderPaginationResponse(BaseModel):
    orders: list[OrderResponse]
    prev_cursor: datetime | None = None
    next_cursor: datetime | None = None
    total_pages: int
    current_page: int


class OrderFilterQuery(BaseModel):
    user_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    status_code: str | None = None
    order_date: date | None = None
    cursor: datetime | None = None
    direction: Literal["next", "prev"] | None = None
    current_page: int | None = None
    page: int | None = None
