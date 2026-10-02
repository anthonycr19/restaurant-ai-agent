from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.producto import Producto


productos_iniciales = [
    {
        "nombre": "lomo saltado",
        "precio": 32.90,
        "stock": 15
    },
    {
        "nombre": "ají de gallina",
        "precio": 28.50,
        "stock": 8
    },
    {
        "nombre": "inca kola",
        "precio": 7.00,
        "stock": 30
    },
]


db = SessionLocal()


try:

    for datos in productos_iniciales:

        statement = select(Producto).where(
            Producto.nombre == datos["nombre"]
        )

        producto_existente = db.scalar(statement)

        if producto_existente is None:

            producto = Producto(**datos)

            db.add(producto)

    db.commit()

    print("Productos cargados correctamente.")

finally:
    db.close()