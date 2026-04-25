from constantes import (
    ERROR_CANTIDAD_INVALIDA,
    ERROR_FORMACION_INVALIDA,
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    PEDIR_DE_NUEVO,
    SALIR,
)
import entrada_de_usuario

def procesar_formacion(formacion_seleccionada: str):
    """Recibe la entrada del usuario, la "splitea" y devuelve la lista creada
    - Si len(lista) es distinto a 3 retorna "pedir de nuevo" e imprime ERROR_FORMACION_INVALIDA
    - Si no cumple el formato devuelve "pedir de nuevo" e imprime ERROR_INPUT_INVALIDO
    """
    if formacion_seleccionada.strip() == "" or formacion_seleccionada.count("-") != 2:
        print(ERROR_INPUT_INVALIDO)
        return PEDIR_DE_NUEVO
    lista_formacion = formacion_seleccionada.split("-")
    if len(lista_formacion) != 3:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO
    suma = 0
    for jugadores_posicion in lista_formacion:
        if not jugadores_posicion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            return PEDIR_DE_NUEVO
        if int(jugadores_posicion) == 0:
            print(ERROR_FORMACION_INVALIDA)
            return PEDIR_DE_NUEVO
        suma += int(jugadores_posicion)
    if suma != 10:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO

    return lista_formacion


def procesar_multiples(
    entrada_del_usuario: str, lista_filtrada: list, cantidad_de_jugadores: int
) -> list | None:
    """Recibe la entrada del usuario de jugadores multiples y verifica
    1. Que no sean duplicados
    2. Que todos sean numeros

    """
    jugadores_seleccionados = entrada_del_usuario.split("-")

    son_numeros = all(jugador.isdigit() for jugador in jugadores_seleccionados)
    if not son_numeros:
        print(ERROR_INPUT_INVALIDO)
        return None

    sin_duplicados = len(jugadores_seleccionados) == len(set(jugadores_seleccionados))
    if not sin_duplicados:
        print(ERROR_INPUT_INVALIDO)
        return None

    if len(jugadores_seleccionados) != int(cantidad_de_jugadores):
        print(ERROR_CANTIDAD_INVALIDA.format(cantidad=cantidad_de_jugadores))
        return None
    lista_jugadores = []
    for indice in jugadores_seleccionados:
        if int(indice) > len(lista_filtrada):
            print(ERROR_SELECCION_INVALIDA)
            return None
        lista_jugadores.append(lista_filtrada[int(indice) - 1])

    return lista_jugadores


def obtener_seleccion_posicion(
    posicion: str, lista_filtrada: list, formacion: list
) -> list:
    """
    Recibe el nombre de la posicion, la lista filtrada segun esa posicion y la formacion como lista
    y llama a la funcion pedir_jugadores.
    - Si esta devuelve "salir" devuelve "salir" y se vuelve al menu principal
    - Sino devuelve una lista con los jugadores seleccionados
    """
    while True:
        jugadores = entrada_de_usuario.pedir_jugadores_alineacion(formacion, posicion, lista_filtrada)
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

def adquirir_formacion(equipos: dict, equipo: str)-> list:
    """Recibe el diccionario de equipos y el nombre del equipo.
    Devuelve una lista con la formacion del equipo."""
    alineacion = equipos[equipo].get("alineacion", {})
    formacion = [
        str(len(alineacion.get("Defensores", []))),
        str(len(alineacion.get("Mediocampistas", []))),
        str(len(alineacion.get("Delanteros", []))),
    ]
    return formacion


def adquirir_jugadores_por_posicion(equipos: dict, equipo: str, posicion: str) -> list | str:
    """Recibe el diccionario de equipos, el nombre del equipo y la posicion.
    Devuelve la lista de jugadores o el nombre del jugador para esa posicion."""
    alineacion = equipos[equipo].get("alineacion", {})
    jugadores = alineacion.get(posicion)
    if not jugadores:
        return [] if posicion in ["Defensores", "Mediocampistas", "Delanteros", "Suplentes"] else ""
    if isinstance(jugadores, list):
        return sorted([jugador[0] for jugador in jugadores]) if posicion != "Suplentes" else sorted(jugadores)
    return jugadores[0]

def adquirir_todas_las_posiciones(equipos, equipo):
    return (
        adquirir_jugadores_por_posicion(equipos,equipo,'Defensores'),
        adquirir_jugadores_por_posicion(equipos,equipo,'Mediocampistas'),
        adquirir_jugadores_por_posicion(equipos,equipo,'Delanteros'),
        adquirir_jugadores_por_posicion(equipos,equipo,'Arquero'),
        adquirir_jugadores_por_posicion(equipos,equipo,'Suplentes'),
        adquirir_jugadores_por_posicion(equipos,equipo,'Capitan')
    )
