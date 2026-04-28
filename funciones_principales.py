from constantes import (
    ERROR_EQUIPO_EXISTENTE,
    ERROR_FORMATO_NOMBRE,
    INPUT_NOMBRE_EQUIPO,
    MSG_EQUIPO_CREADO,
    MSG_ALINEACION_GUARDADA,
    MSG_NO_INFORMACION,
    TEMPLATE_ESTADISTICA_JUGADORES,
    SALIR,
    ENTRADA_SALIR
)
import validaciones
import salida_de_usuario
import entrada_de_usuario
import logica_de_negocio


def crear_equipos(equipos: dict, presupuesto: int):
    """Funcion que permite al usuario crear su equipo.
    Se le pide al usuario que ingrese el nombre de su equipo
    - Si el nombre ya existe imprime ERROR_EQUIPO_EXISTENTE
    - Si el nombre no cumple el formato imprime ERROR_FORMATO_NOMBRE
    """

    while True:
        nombre_equipo = input(INPUT_NOMBRE_EQUIPO)
        if nombre_equipo == ENTRADA_SALIR:
            break
        if validaciones.existe_equipo(nombre_equipo, equipos):
            print(ERROR_EQUIPO_EXISTENTE)
            continue
        if not validaciones.validar_formato_equipo(nombre_equipo):
            print(ERROR_FORMATO_NOMBRE)
            continue

        equipos[nombre_equipo] = {
            "presupuesto": presupuesto,
            "plantel": {
                "Arquero": {},
                "Defensor": {},
                "Mediocampista": {},
                "Delantero": {},
            },
            "alineacion": {
                "Arquero": None,
                "Defensores": [],
                "Mediocampistas": [],
                "Delanteros": [],
                "Capitan": None,
                "Suplentes": [],
                "Titulares": [],
            },
        }
        print(
            MSG_EQUIPO_CREADO.format(
                nombre_equipo=nombre_equipo, presupuesto=presupuesto
            )
        )
        return


def comprar_jugadores(equipos: dict, dataset: list):
    """
    Esta funcion se va a encargar del flujo de ejecucion de las funciones principales
    - Si alguna de las funciones a ejecutar devuelve SALIR se vuelve al menu principal
    """
    while True:
        equipo_seleccionado = salida_de_usuario.mostrar_equipos(equipos)
        if not equipo_seleccionado or equipo_seleccionado == SALIR:
            break
        posicion_seleccionada = salida_de_usuario.mostrar_posiciones(
            equipo_seleccionado,
            equipos,
        )
        if not posicion_seleccionada or posicion_seleccionada == SALIR:
            break
        jugadores_seleccionados = salida_de_usuario.mostrar_jugadores_compra(
            posicion_seleccionada,
            equipo_seleccionado,
            dataset,
            equipos,
        )
        if not jugadores_seleccionados or jugadores_seleccionados == SALIR:
            break
        jugadores_verificados = logica_de_negocio.verificar_presupuesto(
            jugadores_seleccionados,
            equipo_seleccionado,
            equipos,
        )
        if not jugadores_verificados or jugadores_verificados == SALIR:
            break
        if (
            logica_de_negocio.efectuar_compra(
                jugadores_verificados,
                equipo_seleccionado,
                equipos,
            )
            == SALIR
        ):
            break


def vender_jugador(equipos: dict):
    """Esta funcion se va a encargar del flujo de ejecucion de las funciones principales
    del menu de vender jugador.
    - Si alguna de las funciones devuelve SALIR se vuelve al menu principal
    """
    equipo_seleccionado = salida_de_usuario.mostrar_equipos(equipos)
    if not equipo_seleccionado or equipo_seleccionado == SALIR:
        return

    jugador_seleccionado = salida_de_usuario.mostrar_plantel_venta(
        equipo_seleccionado, equipos
    )
    if not jugador_seleccionado or jugador_seleccionado == SALIR:
        return

    if (
        logica_de_negocio.efectuar_venta(
            jugador_seleccionado, equipo_seleccionado, equipos
        )
        == SALIR
    ):
        return


def ver_plantel(equipos: dict):
    """Esta funcion se va a encargar del flujo de ejecucion de las funciones principales
    del menu de ver plantel. Permite ver el plantel de jugadores del equipo seleccionado.
    - Devuelve al menu principal si alguna de las funciones devuelve SALIR
    """
    equipo_seleccionado = salida_de_usuario.mostrar_equipos(equipos)
    if equipo_seleccionado == SALIR:
        return
    salida_de_usuario.mostrar_plantel(equipo_seleccionado, equipos)

def armar_alineacion(equipos: dict):
    """Esta funcion permite crear una alineación de jugadores.
    - Si alguna de las funciones devuelve SALIR o None se vuelve al menú principal.
    """
    while True:
        equipo_seleccionado = salida_de_usuario.mostrar_equipos(equipos)
        if equipo_seleccionado == SALIR:
            break
        formacion_seleccionada = entrada_de_usuario.pedir_formacion(
                    equipo_seleccionado, equipos
                )
        if not formacion_seleccionada or formacion_seleccionada == SALIR:
            break
        alineacion_seleccionada = salida_de_usuario.mostrar_jugadores_alineacion(
            equipos,
            equipo_seleccionado,
            formacion_seleccionada,
        )
        if alineacion_seleccionada == SALIR:
            break
        print(
            MSG_ALINEACION_GUARDADA.format(
                nombre_equipo=equipo_seleccionado
            )
        )
        equipos[equipo_seleccionado]["alineacion"] = alineacion_seleccionada
        break

def ver_alineacion(equipos: dict):
    """Esta funcion imprime la alineación de jugadores del equipo seleccionado.
    - Si alguna de las funciones devuelve SALIR se vuelve al menú principal.
    """
    while True:
        equipo_seleccionado = salida_de_usuario.mostrar_equipos(equipos)
        if equipo_seleccionado == SALIR:
            break
        mensaje = salida_de_usuario.mostrar_alineacion(equipo_seleccionado, equipos)
        if mensaje == SALIR:
            break
        print(mensaje)
        break

def ver_jugador_mas_utilizado(equipos: dict):
    """Recibe el diccionario de equipos e imprime los jugadores más utilizados.
    - Si no hay equipos o conteo de jugadores, imprime MSG_NO_INFORMACION
    - Si no hay al menos una alineacion definida imprime MSG_NO_INFORMACION
    """
    conteo = logica_de_negocio.contar_jugadores(equipos)
    if not equipos or not conteo:
        print(MSG_NO_INFORMACION)
        return

    if not logica_de_negocio.verificar_alineaciones(equipos):
        print(MSG_NO_INFORMACION)
        return

    arquero_max, defensor_max, mediocampista_max, delantero_max = (
        logica_de_negocio.buscar_maximos(conteo)
    )
    arquero_max = arquero_max[0]
    defensor_max = defensor_max[0]
    mediocampista_max = mediocampista_max[0]
    delantero_max = delantero_max[0]
    print(
        TEMPLATE_ESTADISTICA_JUGADORES.format(
            arquero=arquero_max,
            defensor=defensor_max,
            mediocampista=mediocampista_max,
            delantero=delantero_max,
        ).rstrip("\n")
    )
