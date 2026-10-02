import uuid

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.conversacion import Conversacion
from app.models.mensaje import Mensaje


class ConversacionRepository:

    def crear_conversacion(self) -> str:

        db = SessionLocal()

        try:
            conversation_id = str(uuid.uuid4())

            conversacion = Conversacion(
                id=conversation_id
            )

            db.add(conversacion)
            db.commit()

            return conversation_id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    def existe_conversacion(
        self,
        conversation_id: str
    ) -> bool:

        db = SessionLocal()

        try:
            statement = select(Conversacion).where(
                Conversacion.id == conversation_id
            )

            conversacion = db.scalar(statement)

            return conversacion is not None

        finally:
            db.close()


    def guardar_mensaje(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:

        db = SessionLocal()

        try:
            mensaje = Mensaje(
                conversacion_id=conversation_id,
                role=role,
                content=content
            )

            db.add(mensaje)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    def obtener_historial(
        self,
        conversation_id: str
    ) -> list[dict]:

        db = SessionLocal()

        try:
            statement = (
                select(Mensaje)
                .where(
                    Mensaje.conversacion_id == conversation_id
                )
                .order_by(Mensaje.id)
            )

            mensajes = db.scalars(statement).all()

            return [
                {
                    "role": mensaje.role,
                    "content": mensaje.content
                }
                for mensaje in mensajes
            ]

        finally:
            db.close()