from sqlalchemy import DECIMAL, TIMESTAMP, text, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from models import Base
import uuid
from datetime import datetime
import decimal

class Item(Base):
    __tablename__ = "item"

    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.order_id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product.product_id"), nullable=False)
    item_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    item_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    order = relationship("Order")
    product = relationship("Product")

    __table_args__ = (
        PrimaryKeyConstraint("order_id", "product_id"),
    )
