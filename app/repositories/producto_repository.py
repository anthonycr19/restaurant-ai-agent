from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.producto import Producto


class ProductoRepository:

    def buscar_por_nombre(self, nombre: str):

        db = SessionLocal()

        try:

            statement = select(Producto).where(
                Producto.nombre == nombre.lower()
            )

            producto = db.scalar(statement)

            return producto

        finally:
            db.close()


    def actualizar_stock(
        self,
        nombre: str,
        nuevo_stock: int
    ) -> bool:

        db = SessionLocal()

        try:

            statement = select(Producto).where(
                Producto.nombre == nombre.lower()
            )

            producto = db.scalar(statement)

            if producto is None:
                return False

            producto.stock = nuevo_stock

            db.commit()

            return True

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()