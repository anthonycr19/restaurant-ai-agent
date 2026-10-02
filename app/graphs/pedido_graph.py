from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END
from app.agents.restaurante_agent import agent
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from app.services.producto_service import ProductoService

class PedidoState(TypedDict, total=False):

    mensaje: str

    intencion: str

    items: list[dict]

    pedido_pendiente: list[dict]

    esperando_confirmacion: bool

    respuesta: str

    pedido_id: int

    confirmado: bool


def clasificar_intencion(
    state: PedidoState
) -> PedidoState:

    mensaje = state["mensaje"].lower()

    palabras_compra = [
        "quiero",
        "dame",
        "pedir",
        "pedido",
        "comprar"
    ]

    if any(
        palabra in mensaje
        for palabra in palabras_compra
    ):
        return {
            "intencion": "compra"
        }

    return {
        "intencion": "consulta"
    }


def enrutar_intencion(
    state: PedidoState
) -> Literal["consulta", "compra"]:

    if state["intencion"] == "compra":
        return "compra"

    return "consulta"


def procesar_consulta(
    state: PedidoState
) -> PedidoState:

    resultado = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": state["mensaje"]
            }
        ]
    })

    respuesta = resultado["messages"][-1].text

    return {
        "respuesta": respuesta
    }


class ItemPedido(BaseModel):
    nombre: str
    cantidad: int


class ExtraccionPedido(BaseModel):
    items: list[ItemPedido]


modelo_extractor = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning_effort="none"
)

extractor = modelo_extractor.with_structured_output(
    ExtraccionPedido
)

def extraer_pedido(
    state: PedidoState
) -> PedidoState:

    resultado = extractor.invoke(
        f"""
        Extrae los productos y cantidades del siguiente
        pedido de restaurante.

        Mensaje:
        {state["mensaje"]}

        Usa nombres de productos en singular.
        """
    )

    items = [
        {
            "nombre": item.nombre.lower(),
            "cantidad": item.cantidad
        }
        for item in resultado.items
    ]

    return {
        "items": items
    }

producto_service = ProductoService()

def calcular_resumen(
    state: PedidoState
) -> PedidoState:

    items = state["items"]

    detalles = []
    total = 0

    for item in items:

        producto = producto_service.buscar_producto(
            item["nombre"]
        )

        if not producto["encontrado"]:
            return {
                "respuesta": (
                    f"No encontré el producto "
                    f"{item['nombre']}."
                ),
                "esperando_confirmacion": False
            }

        if producto["stock"] < item["cantidad"]:
            return {
                "respuesta": (
                    f"No hay stock suficiente de "
                    f"{producto['nombre']}. "
                    f"Disponibles: {producto['stock']}."
                ),
                "esperando_confirmacion": False
            }

        subtotal = (
            producto["precio"]
            * item["cantidad"]
        )

        detalles.append({
            "nombre": producto["nombre"],
            "cantidad": item["cantidad"],
            "precio_unitario": producto["precio"],
            "subtotal": subtotal
        })

        total += subtotal

    texto = "Resumen del pedido:\n"

    for item in detalles:
        texto += (
            f"\n- {item['cantidad']} "
            f"x {item['nombre']} "
            f"= S/ {item['subtotal']:.2f}"
        )

    texto += (
        f"\n\nTotal: S/ {total:.2f}"
        f"\n\n¿Confirmas el pedido?"
    )

    return {
        "pedido_pendiente": items,
        "esperando_confirmacion": True,
        "respuesta": texto
    }


builder = StateGraph(PedidoState)

builder.add_node(
    "clasificar",
    clasificar_intencion
)

builder.add_node(
    "consulta",
    procesar_consulta
)

builder.add_node(
    "extraer_pedido",
    extraer_pedido
)

builder.add_node(
    "calcular_resumen",
    calcular_resumen
)

builder.add_edge(
    START,
    "clasificar"
)

builder.add_conditional_edges(
    "clasificar",
    enrutar_intencion,
    {
        "consulta": "consulta",
        "compra": "extraer_pedido"
    }
)

builder.add_edge(
    "consulta",
    END
)

builder.add_edge(
    "extraer_pedido",
    "calcular_resumen"
)

builder.add_edge(
    "calcular_resumen",
    END
)

pedido_graph = builder.compile()