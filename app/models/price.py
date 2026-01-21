from sqlalchemy import DECIMAL, TIMESTAMP, text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from models import Base
import uuid
from datetime import datetime, date
import decimal

class Price(Base):
    __tablename__ = "price"

    price_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.product_id"), nullable=False)
    price_amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    product = relationship("Product")
