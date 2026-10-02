from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido


class PedidoRepository:

    def crear_pedido(
        self,
        items: list[dict]
    ) -> dict:

        db = SessionLocal()

        try:

            productos_procesados = []
            total = 0

            # -----------------------------------------
            # 1. Validar y bloquear productos
            # -----------------------------------------

            for item in items:

                nombre = item["nombre"].lower()
                cantidad = item["cantidad"]

                if cantidad <= 0:
                    return {
                        "pedido_creado": False,
                        "mensaje": f"Cantidad inválida para {nombre}"
                    }

                statement = (
                    select(Producto)
                    .where(
                        Producto.nombre == nombre
                    )
                    .with_for_update()
                )

                producto = db.scalar(statement)

                if producto is None:
                    return {
                        "pedido_creado": False,
                        "mensaje": f"Producto no encontrado: {nombre}"
                    }

                if producto.stock < cantidad:
                    return {
                        "pedido_creado": False,
                        "mensaje": f"Stock insuficiente para {nombre}",
                        "stock_disponible": producto.stock
                    }

                subtotal = producto.precio * cantidad

                productos_procesados.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": producto.precio,
                    "subtotal": subtotal
                })

                total += subtotal

            # -----------------------------------------
            # 2. Crear pedido
            # -----------------------------------------

            pedido = Pedido(
                estado="confirmado",
                total=total
            )

            db.add(pedido)
            db.flush()

            # -----------------------------------------
            # 3. Descontar stock y crear detalles
            # -----------------------------------------

            detalles_respuesta = []

            for item in productos_procesados:

                producto = item["producto"]
                cantidad = item["cantidad"]

                producto.stock -= cantidad

                detalle = DetallePedido(
                    pedido_id=pedido.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=item["precio_unitario"],
                    subtotal=item["subtotal"]
                )

                db.add(detalle)

                detalles_respuesta.append({
                    "producto": producto.nombre,
                    "cantidad": cantidad,
                    "precio_unitario": item["precio_unitario"],
                    "subtotal": item["subtotal"],
                    "stock_restante": producto.stock
                })

            # -----------------------------------------
            # 4. Confirmar transacción
            # -----------------------------------------

            db.commit()

            return {
                "pedido_creado": True,
                "pedido_id": pedido.id,
                "items": detalles_respuesta,
                "total": total
            }

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()