from constantes import (
    ERROR_PRESUPUESTO_INSUFICIENTE,
    MSG_VENTA_EXITOSA,
    MSG_ALINEACION_DESARMADA,
    SALIR,
)
import validaciones
import salida_de_usuario

# -------------------------- compra de jugadores -------------------------------------
def verificar_presupuesto(
    jugadores_seleccionados: list, equipo_seleccionado: str, equipos: dict
) -> list | None:
    """Verifica que el presupuesto del equipo alcance para
    la compra de los jugadores seleccionados.
    - Si alcanza devuelve la lista de jugadores_seleccionados
    - Si no alcanza imprime ERROR_PRESUPUESTO_INSUFICIENTE y devuelve None
    """
    monto_total = 0
    for jugador in jugadores_seleccionados:
        monto_total += jugador[2]
    if monto_total <= equipos[equipo_seleccionado]["presupuesto"]:
        return jugadores_seleccionados
    print(ERROR_PRESUPUESTO_INSUFICIENTE)
    return None

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
        equipo = equipos[equipo_seleccionado]
        nombre_jugador = jugador[0]
        posicion_jugador = jugador[1]
        precio_jugador = jugador[2]
        equipo["plantel"][posicion_jugador][nombre_jugador] = {}
        equipo["plantel"][posicion_jugador][nombre_jugador]['precio'] = precio_jugador
        equipo["presupuesto"] -= precio_jugador
        presupuesto_equipo = equipo['presupuesto']
        salida_de_usuario.imprimir_mensaje_compra(nombre_jugador, equipo_seleccionado, presupuesto_equipo)
    return SALIR


# ---------------- venta de jugador --------------------------------------------
def efectuar_venta(jugador_a_vender: tuple, equipo: str, equipos: dict):
    """Efectua la venta del jugador seleccionado, actualizando el presupuesto
    del equipo y el plantel."""
    posicion = jugador_a_vender['posicion']
    nombre_jugador = jugador_a_vender['nombre']
    equipos[equipo]["plantel"][posicion].pop(nombre_jugador)
    equipos[equipo]["presupuesto"] += jugador_a_vender['precio']
    mensaje_de_venta_exitosa = MSG_VENTA_EXITOSA.format(
        nombre_jugador=jugador_a_vender['nombre'],
        presupuesto=equipos[equipo]["presupuesto"],
    )
    if validaciones.esta_en_alineacion(equipo, equipos, jugador_a_vender):
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
                clave_jugador = (jugador['nombre'], jugador['posicion'])
                conteo[clave_jugador] = conteo.get(clave_jugador, 0) + 1
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
