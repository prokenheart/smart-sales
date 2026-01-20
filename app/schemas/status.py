from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class StatusBase(BaseModel):
    status_name: str

class StatusCreate(StatusBase):
    pass

class StatusResponse(StatusBase):
    status_id: uuid.UUID
    updated_at: datetime

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status_name: Optional[str] = None