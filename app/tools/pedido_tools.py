from langchain.tools import tool

from app.services.pedido_service import PedidoService


pedido_service = PedidoService()


@tool
def crear_pedido(
    items: list[dict]
) -> dict:
    """
    Crea un pedido confirmado.

    IMPORTANTE:
    Esta herramienta solo debe utilizarse cuando
    el cliente haya confirmado explícitamente el pedido.

    Cada elemento debe contener:
    - nombre
    - cantidad
    """

    return pedido_service.crear_pedido(
        items=items
    )