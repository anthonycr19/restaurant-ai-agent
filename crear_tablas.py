from app.db.database import Base, engine

from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido
from app.models.conversacion import Conversacion
from app.models.mensaje import Mensaje


print("Creando tablas...")

Base.metadata.create_all(bind=engine)

print("Tablas creadas.")