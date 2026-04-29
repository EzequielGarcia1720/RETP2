from constantes import (
    ROL_RESERVA,
    ROL_SUPLENTE,
    ROL_TITULAR
)
import validaciones
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

def asignar_rol(jugador: dict, equipos: dict, equipo: str)-> str:
    """
    Recibe el diccionario del jugador, el diccionario de equipos y el nombre del equipo
    y segun si se cumple es_suplente o es_titular devuelve el rol correspondiente.

    """
    if validaciones.es_suplente(jugador, equipo, equipos):
        return ROL_SUPLENTE
    if validaciones.es_titular(jugador, equipo, equipos):
        return ROL_TITULAR
    return ROL_RESERVA
    