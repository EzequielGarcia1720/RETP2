def ordenar_jugadores(equipos, equipo):
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
