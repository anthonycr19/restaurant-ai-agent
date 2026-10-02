from app.repositories.pedido_repository import PedidoRepository


class PedidoService:

    def __init__(self):
        self.repository = PedidoRepository()

    def crear_pedido(
        self,
        items: list[dict]
    ) -> dict:

        if not items:
            return {
                "pedido_creado": False,
                "mensaje": "El pedido está vacío"
            }

        return self.repository.crear_pedido(items)