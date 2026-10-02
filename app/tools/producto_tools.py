from langchain.tools import tool

from app.services.producto_service import ProductoService


producto_service = ProductoService()


@tool
def buscar_producto(nombre: str) -> dict:
    """
    Busca un producto y devuelve su precio
    y stock actual.
    """

    return producto_service.buscar_producto(nombre)