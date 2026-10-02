from app.repositories.conversacion_repository import (
    ConversacionRepository
)


class ConversacionService:

    def __init__(self):
        self.repository = ConversacionRepository()


    def obtener_o_crear(
        self,
        conversation_id: str | None
    ) -> str:

        if conversation_id is None:
            return self.repository.crear_conversacion()

        existe = self.repository.existe_conversacion(
            conversation_id
        )

        if not existe:
            raise ValueError(
                "La conversación no existe"
            )

        return conversation_id


    def obtener_historial(
        self,
        conversation_id: str
    ) -> list[dict]:

        return self.repository.obtener_historial(
            conversation_id
        )


    def guardar_usuario(
        self,
        conversation_id: str,
        content: str
    ) -> None:

        self.repository.guardar_mensaje(
            conversation_id=conversation_id,
            role="user",
            content=content
        )


    def guardar_asistente(
        self,
        conversation_id: str,
        content: str
    ) -> None:

        self.repository.guardar_mensaje(
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )