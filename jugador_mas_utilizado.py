def contar_jugadores(equipos: dict)-> dict:
    """Recorre los equipos con alineacion y devuelve un diccionario
    con los jugadores (como tuplas) como claves y su cantidad de apariciones como valores."""
    conteo= {}
    for equipo in equipos.values():
        alineacion = equipo.get("alineacion")
        if not alineacion:
            continue
        tipo_de_jugador = ["Suplentes", "Titulares"]
        for tipo in tipo_de_jugador:
            for jugador in alineacion.get(tipo, []):
                conteo[jugador] = conteo.get(jugador, 0) + 1
    return conteo

def buscar_maximos(conteo: dict)-> list:
    """Recibe el diccionario con el conteo de los jugadores y busca el maximo,
    devuelve una lista de tuplas, siendo cada una el jugador con el maximo de 
    apariciones de cada posicion"""
    posiciones = ["Arquero", "Defensor", "Mediocampista", "Delantero"]
    jugadores_con_mas_apariciones = {
        "Arquero": None,
        "Defensor": None,
        "Mediocampista": None,
        "Delantero": None,
    }
    for posicion in posiciones:
        jugadores_de_posicion = list(
            sorted(jugador for jugador in conteo if jugador[1] == posicion)
        )
        jugadores_con_mas_apariciones[posicion] = max(
            jugadores_de_posicion, key=conteo.get
        )
    return [jugadores_con_mas_apariciones[posicion] for posicion in posiciones]

def verificar_alineaciones(equipos: dict)-> bool:
    """Recibe el diccionario de equipos.
    - Devuelve True si hay al menos dos alineaciones definidas
    - Devuelve False si hay menos de dos alineaciones definidas
    """
    contador = 0
    for equipo in equipos.values():
        alineacion = equipo.get("alineacion")
        if not alineacion:
            continue
        if any(
            alineacion.get(key)
            for key in [
                "Arquero",
                "Capitan",
                "Defensores",
                "Mediocampistas",
                "Delanteros",
                "Suplentes",
                "Titulares",
            ]
        ):
            contador += 1
    return contador >= 2
