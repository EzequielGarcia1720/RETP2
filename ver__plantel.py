from constantes import (
    TEMPLATE_PLANTEL,
    TEMPLATE_JUGADOR_PLANTEL,
    MSG_PLANTEL_VACIO,
    SALIR,
)

# ----------------------- Verificaciones ------------------------

def tiene_jugadores(equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el equipo tiene jugadores en su plantel."""
    return len(equipos[equipo]["plantel"]) > 0


def es_suplente(jugador: tuple, equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el jugador es suplente."""
    if not equipos[equipo].get("alineacion"):
        return False
    return jugador in equipos[equipo]["alineacion"]["Suplentes"]


def es_titular(jugador: tuple, equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el jugador es titular."""
    if not equipos[equipo].get("alineacion"):
        return False
    return jugador in equipos[equipo]["alineacion"]["Titulares"]

# ----------------------- Menúes ------------------------

def mostrar_jugadores(equipo: str, equipos: dict):
    """Recibe el nombre del equipo y el diccionario de equipos. 
    Muestra los jugadores del plantel con su rol (titular, suplente, reserva)
    y su posicion (arquero, defensor, mediocampista, delantero).
    - Si el equipo no tiene jugadores devuelve "salir" y vuelve al
    menu principal e imprime MSG_PLANTEL_VACIO
    - Si el equipo tiene jugadores devuelve True


    """

    mensaje = TEMPLATE_PLANTEL.format(
        nombre_equipo=equipo,
        presupuesto=equipos[equipo]["presupuesto"],
    )
    if not tiene_jugadores(equipo, equipos):
        mensaje += MSG_PLANTEL_VACIO
        print(mensaje)
        return SALIR
    roles = {
        "Titular": "Titular",
        "Suplente": "Suplente",
        "Reserva": "Reserva",
    }
    casos_de_rol = {
        (True, False): lambda: roles["Titular"],
        (False, True): lambda: roles["Suplente"],
        (False, False): lambda: roles["Reserva"],
    }

    contador = 1
    for jugador in sorted(equipos[equipo]["plantel"]):
        rol_actual = casos_de_rol.get(
            (
                es_titular(jugador, equipo, equipos),
                es_suplente(jugador, equipo, equipos),
            )
        )()
        mensaje += TEMPLATE_JUGADOR_PLANTEL.format(
            n=contador,
            nombre_jugador=jugador[0],
            posicion=jugador[1],
            rol_actual=rol_actual,
            precio=jugador[2],
        )
        if contador < len(equipos[equipo]["plantel"]):
            mensaje += "\n"
        contador += 1
    print(mensaje)
    return True
