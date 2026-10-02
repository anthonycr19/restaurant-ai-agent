from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Mensaje(Base):

    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    conversacion_id: Mapped[str] = mapped_column(
        ForeignKey("conversaciones.id"),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    conversacion = relationship(
        "Conversacion",
        back_populates="mensajes"
    )