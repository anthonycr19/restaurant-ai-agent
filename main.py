from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()


# -------------------------------------------------
# "Base de datos" temporal
# -------------------------------------------------

# PRODUCTOS = {
#     "lomo saltado": {
#         "precio": 32.90,
#         "stock": 15,
#     },
#     "ají de gallina": {
#         "precio": 28.50,
#         "stock": 8,
#     },
#     "inca kola": {
#         "precio": 7.00,
#         "stock": 30,
#     },
# }


# -------------------------------------------------
# TOOL
# -------------------------------------------------

from app.tools.producto_tools import buscar_producto
from app.tools.pedido_tools import crear_pedido

# -------------------------------------------------
# MODELO GEMINI
# -------------------------------------------------

modelo = ChatOpenAI(
    model="gpt-5.6-luna",
    reasoning_effort="none"
)


# -------------------------------------------------
# AGENT
# -------------------------------------------------

agent = create_agent(
    model=modelo,
    tools=[
        buscar_producto,
        crear_pedido
    ],
    system_prompt="""
    Eres un agente de atención de un restaurante.

    Cuando el usuario pregunte por un producto:
    - Usa buscar_producto para consultar el producto.
    - No inventes precios ni stock.
    - Interpreta diminutivos, abreviaciones y formas coloquiales
      del nombre de los productos antes de llamar a la herramienta.
    - Por ejemplo, "lomito" puede referirse a "lomo saltado".
    """
)


# -------------------------------------------------
# LOOP DE CONVERSACIÓN
# -------------------------------------------------

historial = []

print("Agente del restaurante")
print("Escribe 'salir' para terminar.\n")

while True:

    mensaje = input("Cliente: ")

    if mensaje.lower() == "salir":
        break

    historial.append({
        "role": "user",
        "content": mensaje
    })

    resultado = agent.invoke({
        "messages": historial
    })

    historial = resultado["messages"]

    respuesta = resultado["messages"][-1].text

    print(f"\nAgente: {respuesta}\n")