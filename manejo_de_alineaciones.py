from constantes import (
    ITEM_LISTA_ALINEACION_ARQUERO,
    ITEM_LISTA_ALINEACION_CAPITAN,
    ITEM_LISTA_ALINEACION_DEFENSORES,
    ITEM_LISTA_ALINEACION_DELANTEROS,
    ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS,
    ITEM_LISTA_ALINEACION_SUPLENTES,
    SALIR,
)
import entrada_de_usuario


def obtener_seleccion_posicion(
    posicion: str, lista_filtrada: list, formacion: list
) -> str | list:
    """
    Recibe el nombre de la posicion, la lista filtrada segun esa posicion y la formacion como lista
    y llama a la funcion pedir_jugadores.
    - Si esta devuelve SALIR devuelve SALIR y se vuelve al menu principal
    - Sino devuelve una lista con los jugadores seleccionados
    """
    while True:
        jugadores = entrada_de_usuario.pedir_jugadores_alineacion(
            formacion, posicion, lista_filtrada
        )
        if jugadores == SALIR:
            return SALIR
        if jugadores:
            return jugadores


def obtener_jugadores_ya_elegidos(alineacion: dict) -> list:
    """
    Recibe el diccionario de la alineacion y devuelve una lista con los jugadores ya elegidos
    """
    elegidos = []
    for valor_posicion in alineacion.values():
        if isinstance(valor_posicion, list):
            elegidos.extend(valor_posicion)
        else:
            elegidos.append(valor_posicion)
    return elegidos


def adquirir_formacion(equipos: dict, equipo: str) -> list:
    """Recibe el diccionario de equipos y el nombre del equipo.
    Devuelve una lista con la formacion del equipo."""
    alineacion = equipos[equipo].get("alineacion", {})
    formacion = [
        str(len(alineacion.get(ITEM_LISTA_ALINEACION_DEFENSORES, []))),
        str(len(alineacion.get(ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS, []))),
        str(len(alineacion.get(ITEM_LISTA_ALINEACION_DELANTEROS, []))),
    ]
    return formacion


def adquirir_jugadores_por_posicion(
    equipos: dict, equipo: str, posicion: str
) -> list | str:
    """Recibe el diccionario de equipos, el nombre del equipo y la posicion.
    Devuelve la lista de jugadores o el nombre del jugador para esa posicion."""
    alineacion = equipos[equipo].get("alineacion", {})
    jugadores = alineacion.get(posicion)
    if not jugadores:
        return (
            []
            if posicion
            in [
                ITEM_LISTA_ALINEACION_DEFENSORES,
                ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS,
                ITEM_LISTA_ALINEACION_DELANTEROS,
                ITEM_LISTA_ALINEACION_SUPLENTES,
            ]
            else ""
        )
    if isinstance(jugadores, list):
        return (
            sorted([jugador["nombre"] for jugador in jugadores])
            if posicion != ITEM_LISTA_ALINEACION_SUPLENTES
            else sorted(jugadores, key=lambda x: x["nombre"])
        )
    return jugadores["nombre"]


def adquirir_todas_las_posiciones(equipos, equipo):
    """
    Devuelve una tupla de listas con los jugadores de cada posicion.
    """
    return (
        adquirir_jugadores_por_posicion(
            equipos, equipo, ITEM_LISTA_ALINEACION_DEFENSORES
        ),
        adquirir_jugadores_por_posicion(
            equipos, equipo, ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS
        ),
        adquirir_jugadores_por_posicion(
            equipos, equipo, ITEM_LISTA_ALINEACION_DELANTEROS
        ),
        adquirir_jugadores_por_posicion(equipos, equipo, ITEM_LISTA_ALINEACION_ARQUERO),
        adquirir_jugadores_por_posicion(
            equipos, equipo, ITEM_LISTA_ALINEACION_SUPLENTES
        ),
        adquirir_jugadores_por_posicion(equipos, equipo, ITEM_LISTA_ALINEACION_CAPITAN),
    )
