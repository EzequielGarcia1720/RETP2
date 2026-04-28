from constantes import (
    ROL_RESERVA,
    ROL_SUPLENTE,
    ROL_TITULAR
)
import validaciones
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

def asignar_rol(jugador, equipos, equipo):
    if validaciones.es_suplente(jugador, equipo, equipos):
        return ROL_SUPLENTE
    if validaciones.es_titular(jugador, equipo, equipos):
        return ROL_TITULAR
    return ROL_RESERVA
    