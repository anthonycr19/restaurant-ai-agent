from app.repositories.producto_repository import ProductoRepository


class ProductoService:

    def __init__(self):
        self.repository = ProductoRepository()


    def buscar_producto(self, nombre: str) -> dict:

        producto = self.repository.buscar_por_nombre(nombre)

        if producto is None:
            return {
                "encontrado": False,
                "mensaje": "Producto no encontrado"
            }

        return {
            "encontrado": True,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock
        }


    def crear_pedido(
        self,
        nombre: str,
        cantidad: int
    ) -> dict:

        producto = self.repository.buscar_por_nombre(nombre)

        if producto is None:
            return {
                "pedido_creado": False,
                "mensaje": "Producto no encontrado"
            }

        if cantidad <= 0:
            return {
                "pedido_creado": False,
                "mensaje": "La cantidad debe ser mayor que cero"
            }

        if producto.stock < cantidad:
            return {
                "pedido_creado": False,
                "mensaje": "Stock insuficiente",
                "stock_disponible": producto.stock
            }

        nuevo_stock = producto.stock - cantidad

        self.repository.actualizar_stock(
            nombre=nombre,
            nuevo_stock=nuevo_stock
        )

        total = producto.precio * cantidad

        return {
            "pedido_creado": True,
            "producto": producto.nombre,
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "total": total,
            "stock_restante": nuevo_stock
        }