from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
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
    prev_cursor_date: datetime | None = None
    prev_cursor_id: uuid.UUID | None = None
    next_cursor_date: datetime | None = None
    next_cursor_id: uuid.UUID | None = None
    total_pages: int
    current_page: int


class OrderFilterQuery(BaseModel):
    user_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    status_code: str | None = None
    order_date: date | None = None
    cursor_date: datetime | None = None
    cursor_id: uuid.UUID | None = None
    direction: Literal["next", "prev"] | None = None
    current_page: int | None = None
    page: int | None = None

    @model_validator(mode="after")
    def validate_pagination_rules(self):
        has_page = self.page is not None

        has_any_cursor_field = any(
            [
                self.cursor_date is not None,
                self.cursor_id is not None,
                self.direction is not None,
                self.current_page is not None,
            ]
        )

        has_full_cursor = all(
            [
                self.cursor_date is not None,
                self.cursor_id is not None,
                self.direction is not None,
                self.current_page is not None,
            ]
        )
        if has_page and has_any_cursor_field:
            raise ValueError(
                "Only one pagination method is allowed: page OR cursor pagination fields"
            )

        if has_any_cursor_field and not has_full_cursor:
            raise ValueError(
                "cursor_date, cursor_id, direction, and current_page must be provided together"
            )

        return self
