from constantes import (
    TEMPLATE_ALINEACION,
    MSG_ALINEACION_INEXISTENTE,
    TEMPLATE_JUGADOR_POSICION,
    SALIR,
)


# -------------------- busquedas ------------------------


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


# def jugadores_en_alineacion(alineacion: dict)-> list:
#     """Recibe el diccionario de la alineacion y devuelve
#     una lista con los jugadores en alineacion."""
#     en_alineacion = []
#     for valor_posicion in alineacion.values():
#         if isinstance(valor_posicion, list):
#             en_alineacion.extend(valor_posicion)
#         else:
#             en_alineacion.append(valor_posicion)
#     return en_alineacion


# def adquirir_defensores(equipos: dict, equipo: str)-> list:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve una lista con los nombres de los defensores del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     return sorted(list(jugador[0] for jugador in alineacion.get("Defensores", [])))


# def adquirir_mediocampistas(equipos: dict, equipo: str)-> list:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve una lista con los nombres de los mediocampistas del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     return sorted(list(jugador[0] for jugador in alineacion.get("Mediocampistas", [])))


# def adquirir_delanteros(equipos: dict, equipo: str)-> list:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve una lista con los nombres de los delanteros del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     return sorted(list(jugador[0] for jugador in alineacion.get("Delanteros", [])))


# def adquirir_arquero(equipos: dict, equipo: str)-> str:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve el nombre del arquero del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     arquero = alineacion.get("Arquero")
#     return arquero[0] if arquero else ""


# def adquirir_suplentes(equipos: dict, equipo: dict)-> list:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve una lista con los nombres de los suplentes del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     return sorted(list(jugador for jugador in alineacion.get("Suplentes", [])))


# def adquirir_capitan(equipos: dict, equipo: str)-> str:
#     """Recibe el diccionario de equipos y el nombre del equipo.
#     Devuelve el nombre del capitan del equipo."""
#     alineacion = equipos[equipo].get("alineacion", {})
#     capitan = alineacion.get("Capitan")
#     return capitan[0] if capitan else ""

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

# ------------------- output -----------------------


def alineacion_inexistente(equipos:dict, equipo: str)-> bool:
    """Recibe el diccionario de equipos y el nombre del equipo.
    Devuelve True si el equipo no tiene alineacion y False si tiene alineacion."""
    alineacion = equipos[equipo].get("alineacion")
    campos = [
        alineacion.get("Arquero"),
        alineacion.get("Capitan"),
        alineacion.get("Defensores"),
        alineacion.get("Mediocampistas"),
        alineacion.get("Delanteros"),
        alineacion.get("Suplentes"),
    ]
    return not any(campos)


def mostrar_alineacion(equipo: str, equipos: dict)-> str:
    """Crea el mensaje con la alineacion del equipo seleccionado.
    - Si el equipo no tiene alineacion imprime MSG_ALINEACION_INEXISTENTE y devuelve "salir"
    Devuelve el mensaje con la alineacion del equipo seleccionado
    """
    if alineacion_inexistente(equipos, equipo):
        print(MSG_ALINEACION_INEXISTENTE)
        return SALIR
    formacion = "-".join(adquirir_formacion(equipos, equipo))
    defensores = adquirir_jugadores_por_posicion(
        equipos, equipo, "Defensores"
    )
    mediocampistas = adquirir_jugadores_por_posicion(
        equipos, equipo, "Mediocampistas"
    )
    delanteros = adquirir_jugadores_por_posicion(
        equipos, equipo, "Delanteros"
    )
    arquero = adquirir_jugadores_por_posicion(
        equipos, equipo, "Arquero"
    )

    suplentes_sin_formato = adquirir_jugadores_por_posicion(
        equipos, equipo, "Suplentes"
    )
    capitan = adquirir_jugadores_por_posicion(
        equipos, equipo, "Capitan"
    )
    mensaje = TEMPLATE_ALINEACION.format(
        formacion=formacion,
        delanteros=" - ".join(delanteros),
        mediocampistas=" - ".join(mediocampistas),
        defensores=" - ".join(defensores),
        arquero=arquero,
        capitan=capitan,
        suplentes="\n".join(
            TEMPLATE_JUGADOR_POSICION.format(
                n=indice, nombre_jugador=jugador[0], posicion=jugador[1]
            )
            for indice, jugador in enumerate(suplentes_sin_formato, start=1)
        ),
    ).rstrip("\n")
    return mensaje
