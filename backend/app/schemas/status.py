from pydantic import BaseModel, ConfigDict, field_validator
import uuid
from datetime import datetime
import re


class StatusBase(BaseModel):
    status_name: str
    status_code: str

    @field_validator("status_code")
    @classmethod
    def validate_status_code(cls, v: str) -> str:
        v = v.upper()

        if not re.fullmatch(r"[A-Z]+", v):
            raise ValueError("status_code must contain only uppercase letters (A-Z)")

        return v


class StatusIdPath(BaseModel):
    status_id: uuid.UUID


class StatusCode(BaseModel):
    status_code: str

    @field_validator("status_code")
    @classmethod
    def validate_status_code(cls, v: str) -> str:
        v = v.upper()

        if not re.fullmatch(r"[A-Z]+", v):
            raise ValueError("status_code must contain only uppercase letters (A-Z)")

        return v


class StatusResponse(StatusBase):
    status_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
