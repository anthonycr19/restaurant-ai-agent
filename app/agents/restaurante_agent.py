from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.tools.producto_tools import buscar_producto
from app.tools.carrito_tools import calcular_pedido
from app.tools.pedido_tools import crear_pedido


modelo = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning_effort="none"
)


agent = create_agent(
    model=modelo,
    tools=[
        buscar_producto,
        crear_pedido,
        calcular_pedido
    ],
    system_prompt="""
    Eres un asistente de ventas de un restaurante peruano.

    Dispones de estas herramientas:

    1. buscar_producto
       Utilízala para consultar precio, stock o disponibilidad.

    2. calcular_pedido
       Utilízala cuando el usuario manifieste intención de compra.
       Esta herramienta solo calcula y valida el pedido.
       No registra nada ni modifica stock.

    3. crear_pedido
       Utilízala únicamente después de que el usuario haya
       confirmado explícitamente el resumen del pedido.

    Proceso obligatorio de compra:

    1. Identifica productos y cantidades.
    2. Usa calcular_pedido.
    3. Presenta al cliente el resumen y total.
    4. Pregunta si desea confirmar.
    5. Solo después de una respuesta afirmativa clara,
       usa crear_pedido.

    Nunca consideres registrado un pedido antes de que
    crear_pedido devuelva pedido_creado=True.

    Nunca inventes precios, stock ni totales.

    Los precios están expresados en soles peruanos.
    """
)

