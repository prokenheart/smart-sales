from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

class StatusBase(BaseModel):
    status_name: str
    status_code: str

class StatusCreate(StatusBase):
    pass

class StatusIdPath(BaseModel):
    status_id: uuid.UUID

class StatusResponse(StatusBase):
    status_id: uuid.UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StatusUpdate(BaseModel):
    status_name: str | None = None
    status_code: str | None = None