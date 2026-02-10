from pydantic import EmailStr, field_validator, ConfigDict
import uuid
from datetime import datetime
import re
from app.schemas.base_schema import CamelCaseModel


class CustomerBase(CamelCaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str

    @field_validator("customer_phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:
        if not v.startswith("+"):
            v = f"+{v}"

        if not re.fullmatch(r"^\+[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number")
        return v


class CustomerCreate(CustomerBase):
    pass


class CustomerIdPath(CamelCaseModel):
    customer_id: uuid.UUID


class CustomerEmailQuery(CamelCaseModel):
    customer_email: EmailStr


class CustomerResponse(CustomerBase):
    customer_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerUpdate(CamelCaseModel):
    customer_name: str | None = None
    customer_email: EmailStr | None = None
    customer_phone: str | None = None

    @field_validator("customer_phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:
        if v is None:
            return v

        if not v.startswith("+"):
            v = f"+{v}"

        if not re.fullmatch(r"^\+[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number")
        return v
