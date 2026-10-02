from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class DetallePedido(Base):

    __tablename__ = "detalle_pedidos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    precio_unitario: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    subtotal: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    pedido = relationship(
        "Pedido",
        back_populates="detalles"
    )