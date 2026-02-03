from sqlalchemy import String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base
import uuid
from datetime import datetime

class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_name: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    customer_phone: Mapped[str] = mapped_column(String(15), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
