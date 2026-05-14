def ordenar_jugadores(equipos: dict, equipo: str)-> list:
    """
    Recibe el diccionario de equipos y el nombre del equipo seleccionado y
    devuelve una lista con los jugadores del plantel ordenados por nombre.
    """
    plantel = equipos[equipo]["plantel"]
    lista = []
    for posicion, jugadores in plantel.items():
        for jugador, detalles in jugadores.items():
            lista.append(
                {
                    "nombre": jugador,
                    "posicion": posicion,
                    "precio": detalles["precio"],
                }
            )
    lista_ordenada = sorted(lista, key=lambda x: x['nombre'])
    return lista_ordenada
