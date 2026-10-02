from app.graphs.pedido_graph import pedido_graph


resultado = pedido_graph.invoke({
    "mensaje": "Quiero 2 lomos saltados y una Inca Kola"
})


print(resultado)
print()
print(resultado["respuesta"])