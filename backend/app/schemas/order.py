from pydantic import ConfigDict, field_validator, model_validator
import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Literal
from app.schemas.status import StatusCode
from app.schemas.base_schema import CamelCaseModel


class OrderBase(CamelCaseModel):
    customer_id: uuid.UUID
    user_id: uuid.UUID


class OrderCreate(OrderBase):
    pass


class OrderIdPath(CamelCaseModel):
    order_id: uuid.UUID


class StatusResponse(CamelCaseModel):
    status_id: uuid.UUID
    status_code: str

    model_config = ConfigDict(from_attributes=True)

class CustomerResponse(CamelCaseModel):
    customer_id: uuid.UUID
    customer_name: str

    model_config = ConfigDict(from_attributes=True)

class UserResponse(CamelCaseModel):
    user_id: uuid.UUID
    user_name: str

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(CamelCaseModel):
    order_id: uuid.UUID
    order_total: Decimal
    order_date: datetime
    order_attachment: str | None
    updated_at: datetime
    status: StatusResponse
    customer: CustomerResponse
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)


class OrderUpdateStatus(StatusCode):
    pass


class OrderDateQuery(CamelCaseModel):
    order_date: datetime


class OrderAttachmentResponse(CamelCaseModel):
    order_id: uuid.UUID
    order_attachment: str

    model_config = ConfigDict(from_attributes=True)


class OrderAttachmentUploadURLRequest(CamelCaseModel):
    content_type: str

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        allowed = {"image/png", "image/jpeg", "application/pdf"}
        if v not in allowed:
            raise ValueError("Unsupported content type")
        return v


class OrderPaginationResponse(CamelCaseModel):
    orders: list[OrderResponse]
    prev_cursor_date: datetime | None = None
    prev_cursor_id: uuid.UUID | None = None
    next_cursor_date: datetime | None = None
    next_cursor_id: uuid.UUID | None = None
    total_pages: int
    current_page: int
    total_orders: int


class OrderFilterQuery(CamelCaseModel):
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
