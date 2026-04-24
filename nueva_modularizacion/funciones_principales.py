from constantes import (
    ERROR_EQUIPO_EXISTENTE,
    ERROR_FORMATO_NOMBRE,
    MSG_EQUIPO_CREADO,
    MSG_ALINEACION_GUARDADA,
    MSG_NO_INFORMACION,
    TEMPLATE_ESTADISTICA_JUGADORES,

)

def crear_equipos(equipos: dict, presupuesto: int):
    """Funcion que permite al usuario crear su equipo.
    Se le pide al usuario que ingrese el nombre de su equipo
    - Si el nombre no cumple el formato imprime ERROR_FORMATO_NOMBRE
    - Si el nombre ya existe imprime ERROR_EQUIPO_EXISTENTE
    """

    while True:
        nombre_equipo = input("Ingrese el nombre de su equipo: ")
        if nombre_equipo == "**":
            break
        if crear_equipo.existe_equipo(nombre_equipo, equipos):
            print(ERROR_EQUIPO_EXISTENTE)
            continue
        if not crear_equipo.validar_formato_equipo(nombre_equipo):
            print(ERROR_FORMATO_NOMBRE)
            continue

        equipos[nombre_equipo] = {
            "presupuesto": presupuesto,
            "plantel": [],
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
    """
    i = 0
    resultados = {}

    variables = [
        "equipo_seleccionado",
        "posicion_seleccionada",
        "jugadores_seleccionados",
        "jugadores_verificados",
        "resultado_compra",
    ]

    while i < len(variables):
        funciones_a_ejecutar = {
            0: lambda: comprar_jugador.mostrar_equipos(equipos),
            1: lambda: comprar_jugador.mostrar_posiciones(
                resultados["equipo_seleccionado"],
                equipos,
            ),
            2: lambda: comprar_jugador.mostrar_jugadores(
                resultados["posicion_seleccionada"],
                resultados["equipo_seleccionado"],
                dataset,
                equipos,
            ),
            3: lambda: comprar_jugador.verificar_presupuesto(
                resultados["jugadores_seleccionados"],
                resultados["equipo_seleccionado"],
                equipos,
            ),
            4: lambda: comprar_jugador.efectuar_compra(
                resultados["jugadores_verificados"],
                resultados["equipo_seleccionado"],
                equipos,
            ),
        }

        resultado_de_funcion = funciones_a_ejecutar[i]()

        if resultado_de_funcion == "salir":
            break
        if resultado_de_funcion is None:
            break

        resultados[variables[i]] = resultado_de_funcion
        i += 1

def vender_jugador(equipos: dict):
    """Esta funcion se va a encargar del flujo de ejecucion de las funciones principales
    del menu de vender jugador."""
    i = 0
    resultados = {}

    variables = [
        "equipo_seleccionado",
        "jugador_seleccionado",
        "resultado_venta",
    ]

    while i < len(variables):
        funciones_a_ejecutar = {
            0: lambda: comprar_jugador.mostrar_equipos(equipos),
            1: lambda: vender.mostrar_jugadores(
                resultados["equipo_seleccionado"], equipos
            ),
            2: lambda: vender.efectuar_venta(
                resultados["jugador_seleccionado"],
                resultados["equipo_seleccionado"],
                equipos,
            ),
        }
        resultado_de_funcion = funciones_a_ejecutar[i]()

        if resultado_de_funcion == "salir":
            break
        if resultado_de_funcion is None:
            break

        resultados[variables[i]] = resultado_de_funcion
        i += 1

def ver_plantel(equipos: dict):
    """Esta funcion se va a encargar del flujo de ejecucion de las funciones principales
    del menu de ver plantel. Permite ver el plantel de jugadores del equipo seleccionado.
    """
    i = 0
    resultados = {}

    variables = [
        "equipo_seleccionado",
        "resultado_plantel",
    ]

    while i < len(variables):
        funciones_a_ejecutar = {
            0: lambda: comprar_jugador.mostrar_equipos(equipos),
            1: lambda: ver__plantel.mostrar_jugadores(
                resultados["equipo_seleccionado"], equipos
            ),
        }
        resultado_de_funcion = funciones_a_ejecutar[i]()

        if resultado_de_funcion == "salir":
            break
        if resultado_de_funcion is None:
            break

        resultados[variables[i]] = resultado_de_funcion
        i += 1

def armar_alineacion(equipos: dict):
    """Esta funcion permite crear una alineación de jugadores.
    - Si alguna de las funciones devuelve "salir" se vuelve al menú principal.
    """
    i = 0
    resultados = {}
    variables = [
        "equipo_seleccionado",
        "formacion_seleccionada",
        "alineacion_seleccionada",
    ]

    while i < len(variables):
        funciones_a_ejecutar = {
            0: lambda: comprar_jugador.mostrar_equipos(equipos),
            1: lambda: armar__alineacion.pedir_formacion(
                resultados["equipo_seleccionado"], equipos
            ),
            2: lambda: armar__alineacion.mostrar_jugadores(
                equipos,
                resultados["equipo_seleccionado"],
                resultados["formacion_seleccionada"],
            ),
        }
        resultado_de_funcion = funciones_a_ejecutar[i]()

        if resultado_de_funcion == "salir":
            break
        resultados[variables[i]] = resultado_de_funcion
        i += 1
    if i == 3:
        print(
            MSG_ALINEACION_GUARDADA.format(
                nombre_equipo=resultados["equipo_seleccionado"]
            )
        )
        equipos[resultados["equipo_seleccionado"]]["alineacion"] = resultados[
            "alineacion_seleccionada"
        ]

def ver_alineacion(equipos: dict):
    """Esta funcion imprime la alineación de jugadores del equipo seleccionado.
    - Si alguna de las funciones devuelve "salir" se vuelve al menú principal.
    """
    i = 0
    resultados = {}
    variables = [
        "equipo_seleccionado",
        "mensaje",
    ]
    while i < len(variables):
        funciones_a_ejecutar = {
            0: lambda: comprar_jugador.mostrar_equipos(equipos),
            1: lambda: ver__alineacion.mostrar_alineacion(
                resultados["equipo_seleccionado"], equipos
            ),
        }

        resultado_de_funcion = funciones_a_ejecutar[i]()

        if resultado_de_funcion == "salir":
            break
        resultados[variables[i]] = resultado_de_funcion
        i += 1
    if i == 2:
        print(resultados["mensaje"])

def ver_jugador_mas_utilizado(equipos: dict):
    """Recibe el diccionario de equipos e imprime los jugadores más utilizados.
    - Si no hay equipos o conteo de jugadores, imprime MSG_NO_INFORMACION
    - Si no hay al menos dos alineaciones definidas imprime MSG_NO_INFORMACION
    """
    conteo = jugador_mas_utilizado.contar_jugadores(equipos)
    if not equipos or not conteo:
        print(MSG_NO_INFORMACION)
        return

    if not jugador_mas_utilizado.verificar_alineaciones(equipos):
        print(MSG_NO_INFORMACION)
        return

    arquero_max, defensor_max, mediocampista_max, delantero_max = (
        jugador_mas_utilizado.buscar_maximos(conteo)
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
        )
    )