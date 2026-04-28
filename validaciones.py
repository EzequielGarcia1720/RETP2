# funciones de crear equipo
from constantes import (
    ALINEACION_ARQUERO,
    ALINEACION_CAPITAN,
    ERROR_JUGADOR_EXISTENTE,
    LISTA_ALINEACION_DEFENSORES,
    LISTA_ALINEACION_DELANTEROS,
    LISTA_ALINEACION_MEDIOCAMPISTAS,
    LISTA_ALINEACION_SUPLENTES,
    LISTA_ALINEACION_TITULARES,
    LISTA_PLANTEL_ARQUERO,
    LISTA_PLANTEL_DEFENSOR,
    LISTA_PLANTEL_DELANTERO,
    LISTA_PLANTEL_MEDIOCAMPISTA,
    MSG_CANTIDAD_JUGADORES_INSUFICIENTE,
    LARGO_MAX_NOMBRE_EQUIPO,
    MINIMO_JUGADORES_EN_PLANTEL,
)
import manejo_de_equipos


def validar_formato_equipo(nombre_equipo):
    """Funcion que valida el nombre del equipo ingresado. El nombre no debe contener numeros,
    caracteres especiales, exceder los 50 caracteres ni ser una cadena vacia. Si el nombre es
    valido, se retorna True, de lo contrario se retorna False."""
    if (
        len(nombre_equipo) > LARGO_MAX_NOMBRE_EQUIPO
        or len(nombre_equipo) == 0
        or nombre_equipo.isdigit()
        or nombre_equipo.rstrip() == ""
    ):
        return False
    for caracter in nombre_equipo:
        if not caracter.isalpha() and not caracter.isspace():
            return False
    return True


def existe_equipo(nombre_equipo, equipos):
    """Funcion que verifica si el equipo ya existe.
    Si el equipo existe, se retorna True, de lo contrario se retorna False."""
    return nombre_equipo in equipos


# Funciones Comprar jugador
def procesar_multiples(entrada_del_usuario: str, input_err_msg: str) -> list:
    """Recibe la entrada del usuario de jugadores multiples y verifica
    1. Que no sean duplicados
    2. Que todos sean numeros
    En ambos casos de error imprime ERROR_INPUT_INVALIDO y devuelve None
    De ser valido devuelve una lista con los numeros ingresados
    """
    jugadores_seleccionados = entrada_del_usuario.split("-")

    son_numeros = all(jugador.isdigit() for jugador in jugadores_seleccionados)
    sin_duplicados = len(jugadores_seleccionados) == len(set(jugadores_seleccionados))

    if not sin_duplicados:
        print(input_err_msg)
        return None

    if not son_numeros:
        print(input_err_msg)
        return None

    return jugadores_seleccionados


def verificar_existencia_jugador(
    jugadores_seleccionados: list, equipo_seleccionado: str, equipos: dict
) -> bool:
    """Verifica que el jugador seleccionado no exista en el equipo seleccionado
    - Si existe imprime ERROR_JUGADOR_EXISTENTE
    - Si no existe devuelve True
    """
    contador = 0
    plantel = equipos[equipo_seleccionado]["plantel"]
    for jugador in jugadores_seleccionados:
        posicion = jugador[1]
        nombre_jugador = jugador[0]
        if plantel[posicion].get(nombre_jugador, None):
            print(ERROR_JUGADOR_EXISTENTE.format(nombre_jugador=jugador[0]))
            contador += 1
    if contador > 0:
        return False
    return True


# Vender jugadores


def tiene_jugadores(equipo: str, equipos: dict) -> bool:
    """Funcion que verifica si el equipo tiene jugadores en su plantel.
    - Devuelve True si el equipo tiene jugadores
    - Devuelve False si el equipo no tiene jugadores
    """
    posiciones = [
        LISTA_PLANTEL_ARQUERO,
        LISTA_PLANTEL_DEFENSOR,
        LISTA_PLANTEL_MEDIOCAMPISTA,
        LISTA_PLANTEL_DELANTERO,
    ]
    return any(len(equipos[equipo]["plantel"][posicion]) > 0 for posicion in posiciones)


def es_suplente(jugador: tuple, equipo: str, equipos: dict) -> bool:
    """Funcion que verifica si el jugador es suplente.
    - Devuelve True si el jugador es suplente
    - Devuelve False si el jugador no es suplente
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False
    return jugador in alineacion.get(LISTA_ALINEACION_SUPLENTES, [])


def es_titular(jugador: tuple, equipo: str, equipos: dict) -> bool:
    """Funcion que verifica si el jugador es titular.
    - Devuelve True si el jugador es titular
    - Devuelve False si el jugador no es titular
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False
    return jugador in alineacion.get(LISTA_ALINEACION_TITULARES, [])


def esta_en_alineacion(equipo: str, equipos: dict, jugador: tuple) -> bool:
    """Funcion que verifica si el jugador esta en la alineacion.
    - Si no hay alineacion devuelve False
    - Si está en la alineacion devuelve True
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False

    # No agrego al arquero porque en el diccionario es una tupla, no una lista de tuplas
    posiciones = {
        LISTA_PLANTEL_DEFENSOR: LISTA_ALINEACION_DEFENSORES,
        LISTA_PLANTEL_MEDIOCAMPISTA: LISTA_ALINEACION_MEDIOCAMPISTAS,
        LISTA_PLANTEL_DELANTERO: LISTA_ALINEACION_DELANTEROS,
    }

    posicion = posiciones.get(jugador["posicion"])
    if posicion and jugador in alineacion.get(posicion, []):
        return True

    return jugador == alineacion.get(ALINEACION_ARQUERO) or jugador in alineacion.get(
        LISTA_ALINEACION_SUPLENTES, []
    )


# Armar alineacion


def verificar_cant_jugadores(
    equipo: str, equipos: dict, formacion_seleccionada: list
) -> bool:
    """Recibe el equipo seleccionado, el diccionario de equipos y la lista con la formacion
    seleccionada.
    - Si la cantidad de jugadores en el plantel es menor a 16 devuelve False
    - Si no hay jugadores suficientes para la formacion seleccionada devuelve False
    - Sino devuelve True
    """
    plantel = manejo_de_equipos.ordenar_jugadores(equipos, equipo)
    if len(plantel) < MINIMO_JUGADORES_EN_PLANTEL:
        print(MSG_CANTIDAD_JUGADORES_INSUFICIENTE)
        return False
    arqueros = len(equipos[equipo]["plantel"][LISTA_PLANTEL_ARQUERO])
    defensores = len(equipos[equipo]["plantel"][LISTA_PLANTEL_DEFENSOR])
    mediocampistas = len(equipos[equipo]["plantel"][LISTA_PLANTEL_MEDIOCAMPISTA])
    delanteros = len(equipos[equipo]["plantel"][LISTA_PLANTEL_DELANTERO])
    if (
        arqueros < 1
        or defensores < int(formacion_seleccionada[0])
        or mediocampistas < int(formacion_seleccionada[1])
        or delanteros < int(formacion_seleccionada[2])
    ):
        print(MSG_CANTIDAD_JUGADORES_INSUFICIENTE)
        return False
    return True


def alineacion_inexistente(equipos: dict, equipo: str) -> bool:
    """Recibe el diccionario de equipos y el nombre del equipo.
    Devuelve True si el equipo no tiene alineacion y False si tiene alineacion."""
    alineacion = equipos[equipo].get("alineacion")
    campos = [
        alineacion.get(ALINEACION_ARQUERO),
        alineacion.get(ALINEACION_CAPITAN),
        alineacion.get(LISTA_ALINEACION_DEFENSORES),
        alineacion.get(LISTA_ALINEACION_MEDIOCAMPISTAS),
        alineacion.get(LISTA_ALINEACION_DELANTEROS),
        alineacion.get(LISTA_ALINEACION_SUPLENTES),
    ]
    return not any(campos)
