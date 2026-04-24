from constantes import (
    MSG_COMPRA_EXITOSA,
    MSG_VENTA_EXITOSA,
    MSG_ALINEACION_DESARMADA,
)


# -------------------------- compra de jugadores -------------------------------------
def efectuar_compra(
    jugadores_seleccionados: list, equipo_seleccionado: str, equipos: dict
):
    """Efectua la compra de los jugadores seleccionados para el equipo seleccionado
    Recibe:
        - Una lista con los jugadores seleccionados
        - El equipo seleccionado
        - El diccionario de equipos
    POSTCONDICIONES:
        Imprime MSG_COMPRA_EXITOS para cada jugador comprado
        Resta el precio del jugador al presupuesto del equipo seleccionado
        Appendea o agrega el jugador a la lista "plantel" del diccionario del equipo seleccionado
    """
    jugadores_seleccionados = sorted(jugadores_seleccionados)
    for jugador in jugadores_seleccionados:
        equipos[equipo_seleccionado]["plantel"].append(jugador)
        equipos[equipo_seleccionado]["presupuesto"] -= jugador[2]
# El print podria ponerlo en una funcion y ponerlo junto a todo el output
        print(
            MSG_COMPRA_EXITOSA.format(
                nombre_jugador=jugador[0],
                nombre_equipo=equipo_seleccionado,
                presupuesto=equipos[equipo_seleccionado]["presupuesto"],
            )
        )

# ---------------- venta de jugador --------------------------------------------
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


# -------------- Jugadores más utilizados -------------------------

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
    return contador >= 1