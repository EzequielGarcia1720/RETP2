from constantes import (
    CANTIDAD_VALORES_FORMACION,
    ERROR_CANTIDAD_INVALIDA,
    ERROR_FORMACION_INVALIDA,
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    ITEM_LISTA_ALINEACION_ARQUERO,
    ITEM_LISTA_ALINEACION_CAPITAN,
    ITEM_LISTA_ALINEACION_DEFENSORES,
    ITEM_LISTA_ALINEACION_DELANTEROS,
    ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS,
    ITEM_LISTA_ALINEACION_SUPLENTES,
    PEDIR_DE_NUEVO,
    SALIR,
    MINIMO_JUGADORES_EN_FORMACION,
)
import entrada_de_usuario


def procesar_formacion(formacion_seleccionada: str) -> str | list:
    """Recibe la entrada del usuario, la "splitea" y devuelve la lista creada
    - Si len(lista) es distinto a CANTIDAD_VALORES_FORMACION devuelve PEDIR_DE_NUEVO
    e imprime ERROR_FORMACION_INVALIDA
    - Si no cumple el formato devuelve PEDIR_DE_NUEVO e imprime ERROR_INPUT_INVALIDO
    """
    if formacion_seleccionada.strip() == "" or formacion_seleccionada.count("-") != 2:
        print(ERROR_INPUT_INVALIDO)
        return PEDIR_DE_NUEVO
    lista_formacion = formacion_seleccionada.split("-")
    if len(lista_formacion) != CANTIDAD_VALORES_FORMACION:
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
    if suma != MINIMO_JUGADORES_EN_FORMACION:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO

    return lista_formacion


def procesar_multiples(
    entrada_del_usuario: str, lista_filtrada: list, cantidad_de_jugadores: int
) -> list | None:
    """Recibe la entrada del usuario de jugadores multiples y verifica
    1. Que no sean duplicados -> sino imprime ERROR_INPUT_INVALIDO y devuelve None
    2. Que todos sean numeros -> sino imprime ERROR_INPUT_INVALIDO y devuelve None
    3. Que la cantidad de jugadores seleccionados no sea distinta a cantidad_de_jugadores ->
    sino imprime ERROR_CANTIDAD_INVALIDA y devuelve None
    4. Que los índices ingresados estén dentro del rango de la lista_filtrada
        -> sino imprime ERROR_SELECCION_INVALIDA y devuelve None
    De ser válida devuelve una lista con los diccionarios de los jugadores seleccionados.

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
            if posicion != "Suplentes"
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
