from langchain.tools import tool

from app.services.producto_service import ProductoService


producto_service = ProductoService()


@tool
def calcular_pedido(items: list[dict]) -> dict:
    """
    Calcula el resumen de un pedido sin registrarlo.

    Cada item debe tener:
    - nombre
    - cantidad

    No modifica stock ni crea pedidos.
    """

    detalle = []
    total = 0

    for item in items:

        nombre = item["nombre"]
        cantidad = item["cantidad"]

        if cantidad <= 0:
            return {
                "valido": False,
                "mensaje": f"Cantidad inválida para {nombre}"
            }

        producto = producto_service.buscar_producto(nombre)

        if not producto["encontrado"]:
            return {
                "valido": False,
                "mensaje": f"Producto no encontrado: {nombre}"
            }

        if producto["stock"] < cantidad:
            return {
                "valido": False,
                "mensaje": f"Stock insuficiente para {nombre}",
                "stock_disponible": producto["stock"]
            }

        subtotal = producto["precio"] * cantidad

        detalle.append({
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio_unitario": producto["precio"],
            "subtotal": subtotal
        })

        total += subtotal

    return {
        "valido": True,
        "items": detalle,
        "total": total
    }