from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Pedido(Base):

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="confirmado"
    )

    total: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    detalles = relationship(
        "DetallePedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )
