from fastapi import APIRouter, HTTPException

from app.agents.restaurante_agent import agent
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversacion_service import ConversacionService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


conversacion_service = ConversacionService()


@router.post(
    "",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:
        conversation_id = (
            conversacion_service.obtener_o_crear(
                request.conversation_id
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    # 1. Recuperamos historial anterior
    historial = conversacion_service.obtener_historial(
        conversation_id
    )

    # 2. Agregamos el nuevo mensaje del usuario
    historial.append({
        "role": "user",
        "content": request.message
    })

    # 3. Ejecutamos el agente
    resultado = agent.invoke({
        "messages": historial
    })

    respuesta = resultado["messages"][-1].text

    # 4. Persistimos el mensaje del usuario
    conversacion_service.guardar_usuario(
        conversation_id=conversation_id,
        content=request.message
    )

    # 5. Persistimos la respuesta
    conversacion_service.guardar_asistente(
        conversation_id=conversation_id,
        content=respuesta
    )

    return ChatResponse(
        conversation_id=conversation_id,
        response=respuesta
    )