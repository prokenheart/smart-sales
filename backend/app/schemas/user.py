from pydantic import EmailStr, Field, field_validator, ConfigDict
import uuid
from datetime import datetime
import re
from app.schemas.base_schema import CamelCaseModel


class UserBase(CamelCaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_account: str
    user_password: str = Field(..., min_length=8)

    @field_validator("user_phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:
        if not v.startswith("+"):
            v = f"+{v}"

        if not re.fullmatch(r"^\+[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number")
        return v


class UserCreate(UserBase):
    pass


class UserIdPath(CamelCaseModel):
    user_id: uuid.UUID


class UserEmailQuery(CamelCaseModel):
    user_email: EmailStr


class UserResponse(CamelCaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_account: str
    user_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateInfo(CamelCaseModel):
    user_name: str | None = None
    user_email: EmailStr | None = None
    user_phone: str | None = None

    @field_validator("user_phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:
        if v is None:
            return v

        if not v.startswith("+"):
            v = f"+{v}"

        if not re.fullmatch(r"^\+[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number")
        return v


class UserUpdatePassword(CamelCaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
