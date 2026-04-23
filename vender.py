from constantes import (
    TEMPLATE_PLANTEL,
    TEMPLATE_JUGADOR_PLANTEL,
    MSG_PLANTEL_VACIO,
    MSG_VENTA_EXITOSA,
    MSG_ALINEACION_DESARMADA,
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    SALIR,
)

# ----------------------- Verificaciones ------------------------


def tiene_jugadores(equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el equipo tiene jugadores en su plantel.
    - Devuelve True si el equipo tiene jugadores
    - Devuelve False si el equipo no tiene jugadores
    """
    return len(equipos[equipo]["plantel"]) > 0


def es_suplente(jugador: tuple, equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el jugador es suplente.
    - Devuelve True si el jugador es suplente
    - Devuelve False si el jugador no es suplente
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False
    return jugador in alineacion.get("Suplentes", [])


def es_titular(jugador: tuple, equipo: str, equipos: dict)-> bool:
    """Funcion que verifica si el jugador es titular.
    - Devuelve True si el jugador es titular
    - Devuelve False si el jugador no es titular
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False
    return jugador in alineacion.get("Titulares", [])


def esta_en_alineacion(equipo: str, equipos: dict, jugador: tuple)-> bool:
    """Funcion que verifica si el jugador esta en la alineacion.
    - Si no hay alineacion devuelve False
    - Si está en la alineacion devuelve True
    """
    alineacion = equipos[equipo].get("alineacion")
    if not alineacion:
        return False

    # No agrego al arquero porque en el diccionario es una tupla, no una lista de tuplas
    posiciones = {
        "Defensor": "Defensores",
        "Mediocampista": "Mediocampistas",
        "Delantero": "Delanteros",
    }

    posicion = posiciones.get(jugador[1])
    if posicion and jugador in alineacion.get(posicion, []):
        return True

    return jugador == alineacion.get("Arquero") or jugador in alineacion.get("Suplentes", [])


# ----------------------- Inputs ------------------------


def pedir_entrada(equipo: str, equipos: dict)-> str | None:
    """Funcion que pide la entrada del jugador a vender.
    - Si la entrada es "**" devuelve "salir" y vuelve al menu principal
    - Si la entrada no es un numero imprime ERROR_INPUT_INVALIDO y devuelve None
    - Si la entrada es menor a 1 o mayor a la cantidad de jugadores en el plantel
    imprime ERROR_SELECCION_INVALIDA y devuelve None
    - Si la entrada es valida devuelve la entrada del usuario
    """
    entrada_del_usuario = input("Seleccione el jugador a vender: ")
    if entrada_del_usuario == "**":
        return SALIR
    if not entrada_del_usuario.isdigit():
        print(ERROR_INPUT_INVALIDO)
        return None
    if int(entrada_del_usuario) < 1 or int(entrada_del_usuario) > len(
        equipos[equipo]["plantel"]
    ):
        print(ERROR_SELECCION_INVALIDA)
        return None
    return entrada_del_usuario


# ----------------------- Menúes ------------------------


def mostrar_jugadores(equipo: str, equipos: dict)-> str | None | tuple:
    """Funcion que muestra los jugadores del plantel y llama a la funcion pedir_entrada.
    Recibe el equipo seleccionado y el diccionario de equipos.
    - Si el equipo seleccionado no tiene jugadores vuelve al menu 
    principal e imprime MSG_PLANTEL_VACIO
    - Si pedir_entrada devuelve "salir" devuelve "salir" y vuelve al menu principal
    - Si pedir_entrada devuelve None vuelve a empezar el while solicitando entrada
    nuevamente.
    - Si la entrada es valida devuelve la tupla del jugador a vender.

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
    while True:
        jugador_a_vender = pedir_entrada(equipo, equipos)
        if jugador_a_vender == SALIR:
            return SALIR
        if jugador_a_vender is None:
            continue
        jugador_a_vender = sorted(equipos[equipo]["plantel"])[int(jugador_a_vender) - 1]

        # Para ver que se imprima devuelva el correcto fjfjjf
        # print(jugador_a_vender)

        return jugador_a_vender


def efectuar_venta(jugador_a_vender: tuple, equipo: str, equipos: dict):
    """Efectua la venta del jugador seleccionado, actualizando el presupuesto
    del equipo y el plantel."""
    equipos[equipo]["plantel"].remove(jugador_a_vender)
    equipos[equipo]["presupuesto"] += jugador_a_vender[2]
    mensaje_de_venta_exitosa = MSG_VENTA_EXITOSA.format(
        nombre_jugador=jugador_a_vender[0],
        presupuesto=equipos[equipo]["presupuesto"],
    )
    if esta_en_alineacion(equipo, equipos, jugador_a_vender):
        mensaje_de_venta_exitosa += "\n" + MSG_ALINEACION_DESARMADA
        if "alineacion" in equipos[equipo]:
            equipos[equipo]["alineacion"] = {
                "Arquero": None,
                "Defensores": [],
                "Mediocampistas": [],
                "Delanteros": [],
                "Capitan": None,
                "Suplentes": [],
                "Titulares": [],
            }
    print(mensaje_de_venta_exitosa)
