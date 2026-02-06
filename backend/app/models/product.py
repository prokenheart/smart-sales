from sqlalchemy import String, Integer, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models import Base
import uuid
from datetime import datetime


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    product_description: Mapped[str] = mapped_column(String(255), nullable=True)
    product_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")
    )
