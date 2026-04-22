# Imports
from constantes import (
    MSG_COMPRA_EXITOSA,
    TEMPLATE_PRESUPUESTO,
    TEMPLATE_JUGADOR_PRECIO,
    TEMPLATE_EQUIPO,
    ERROR_PRESUPUESTO_INSUFICIENTE,
    ERROR_JUGADOR_EXISTENTE,
    ERROR_SIN_EQUIPOS,
    ERROR_SELECCION_INVALIDA,
    HEADER_EQUIPOS,
    HEADER_JUGADORES,
    ERROR_INPUT_INVALIDO,
)


# ----------------------------------- Validaciones ----------------------------------------------


def procesar_multiples(entrada_del_usuario: str, input_err_msg: str)-> list:
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
    for jugador in jugadores_seleccionados:
        if jugador in equipos[equipo_seleccionado]["plantel"]:
            print(ERROR_JUGADOR_EXISTENTE.format(nombre_jugador=jugador[0]))
            contador += 1
    if contador > 0:
        return False
    return True


def identificar_entrada(
    entrada_del_usuario: str | int,
    sel_inv_err_msg: str,
    input_err_msg: str,
    maximo: int,
) -> list | None:
    """Identifica si la entrada del usuario corresponde a una compra individual o multiple.
    - Si la entrada es un numero entero menor o igual a 5, se considera una compra individual
    y se retorna un solo numero en la lista.
    - Si la entrada es una lista de numeros menor o iguales a 5 separados por guiones,
    se considera una compra multiple y se retorna una lista de numeros."""

    es_individual = entrada_del_usuario.lstrip("-").isdigit()
    es_multiple = "-" in entrada_del_usuario

    casos_de_entrada = {
        (True, False): lambda: [entrada_del_usuario],
        (False, True): lambda: procesar_multiples(entrada_del_usuario, input_err_msg),
    }
    jugadores_seleccionados = casos_de_entrada.get(
        (es_individual, es_multiple), lambda: print(sel_inv_err_msg)
    )()
    if jugadores_seleccionados is None:
        return None
    for indice in jugadores_seleccionados:
        if int(indice) > maximo or int(indice) < 1:
            print(sel_inv_err_msg)
            return None

    return jugadores_seleccionados


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


# ------------------------------------ Búsquedas ------------------------------------------------


def filtrar_jugadores_por_posicion(posicion: str, dataset: list):
    """Filtra los jugadores disponibles por posicion y retorna una lista de jugadores filtrada"""
    return [jugador for jugador in dataset if jugador[1] == posicion]


# -------------------------------------- Inputs -------------------------------------------------


def pedir_entero(mensaje_input: str, minimo: int, maximo: int) -> int:
    """Solicita un numero entero al usuario y lo valida.
    Recibe un mensaje que se imprime a la hora de hacer el input y dos valores enteros,
    el maximo y el minimo de valores que puede tomar el input como validos.
    - En caso de no ser un numero entero muestra ERROR_INPUT_INVALIDO
    - En caso de no estar entre minimo y maximo muestra ERROR_SELECCION_INVALIDA
    - En caso de ser valido devuelve el numero entero ingresado
    - En caso de ingresar "**" devuelve None y vuelve al menu principal
    """
    opcion_seleccionada = input(mensaje_input)
    if opcion_seleccionada == "**":
        return None

    while True:
        if not opcion_seleccionada.isdigit():
            print(ERROR_INPUT_INVALIDO)
            opcion_seleccionada = input("Seleccione una opción: ")
            if opcion_seleccionada == "**":
                return None
            continue
        if int(opcion_seleccionada) < minimo or int(opcion_seleccionada) > maximo:
            print(ERROR_SELECCION_INVALIDA)
            opcion_seleccionada = input("Seleccione una opción: ")
            if opcion_seleccionada == "**":
                return None
            continue
        return int(opcion_seleccionada)


def pedir_jugadores(
    jugadores_disponibles: list,
    pagina_actual: int,
    nombre_equipo: str,
    equipos: dict,
):
    """
    Pide entrada al usuario para seleccionar jugadores.
    Para ser valida la entrada del usuario debe ser:
        - "**" para salir al menu principal
        - "<" o ">" para moverse entre paginas (en caso de ser posible, sino imprime
        ERROR_SELECCION_INVALIDA y vuelve a pedir entrada)
        - En cualquier otro caso verifica la entrada, de ser invalida vuelve a pedir entrada,
        en caso de ser valida devuelve una lista con las tuplas de cada jugador seleccionado.
    """
    resultado_a_devolver = None
    pagina = pagina_actual
    maximo = min(5, len(jugadores_disponibles) - pagina * 5)

    entrada_del_usuario = input(
        "> : Siguiente página\n< : Página anterior\nSeleccione una opcion: "
    )

    while True:
        match entrada_del_usuario:
            case "**":
                resultado_a_devolver = "salir"
                break

            case "<":
                if pagina > 0:
                    resultado_a_devolver = pagina - 1
                    break

                print(ERROR_SELECCION_INVALIDA)
                entrada_del_usuario = input("Seleccione una opcion: ")
                continue

            case ">":
                if (pagina + 1) * 5 < len(jugadores_disponibles):
                    resultado_a_devolver = pagina + 1
                    break

                print(ERROR_SELECCION_INVALIDA)
                entrada_del_usuario = input("Seleccione una opcion: ")
                continue

            case _:
                indices_de_jugadores = identificar_entrada(
                    entrada_del_usuario,
                    ERROR_SELECCION_INVALIDA,
                    ERROR_INPUT_INVALIDO,
                    maximo,
                )

                if not indices_de_jugadores:
                    entrada_del_usuario = input("Seleccione una opcion: ")
                    continue

                lista_jugadores = []
                for indice in indices_de_jugadores:
                    indice_real = (pagina_actual * 5) + int(indice) - 1
                    lista_jugadores.append(jugadores_disponibles[indice_real])
                if not verificar_existencia_jugador(
                    lista_jugadores, nombre_equipo, equipos
                ):
                    entrada_del_usuario = input("Seleccione una opcion: ")
                    continue

                resultado_a_devolver = lista_jugadores
                break
    return resultado_a_devolver


# -------------------------------------- Menúes -------------------------------------------------


def mostrar_equipos(equipos: dict) -> str:
    """Muestra los equipos disponibles para comprar jugadores y llama la
    funcion pedir_entero para que el usuario seleccione un equipo
    - Si equipo seleccionado es None devuelve "salir"
    - Si no hay equipos disponibles imprime ERROR_SIN_EQUIPOS y retorna "salir"
    - Si equipo seleccionado es valido devuelve el nombre del equipo
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return "salir"
    opciones = sorted(list(equipos))
    maximo = len(opciones)
    mensaje = HEADER_EQUIPOS
    for indice, opcion in enumerate(opciones, start=1):
        mensaje += "\n" + TEMPLATE_EQUIPO.format(n=indice, nombre_equipo=opcion)
    print(mensaje)
    mensaje_input = "Seleccione un equipo: "
    equipo_seleccionado = pedir_entero(mensaje_input, 1, maximo)
    if equipo_seleccionado is None:
        return "salir"
    return opciones[int(equipo_seleccionado) - 1]


def mostrar_posiciones(nombre_equipo: str, equipos: dict) -> str:
    """Muestra las posiciones disponibles para comprar jugadores y llama la
    funcion pedir_entero para que el usuario seleccione una posicion
    - Si posicion seleccionada es None retorna "salir"
    - Si la posicion seleccionada es valida devuelve la posicion
    """
    posiciones = ["Arquero", "Defensor", "Mediocampista", "Delantero"]
    print(
        TEMPLATE_PRESUPUESTO.format(presupuesto=equipos[nombre_equipo]["presupuesto"])
    )
    mensaje_input = "Posiciones:\n1. Arquero\n2. Defensor\n3. Mediocampista\n4. Delantero\nSeleccione una opcion: "
    posicion_seleccionada = pedir_entero(mensaje_input, 1, len(posiciones))
    if posicion_seleccionada is None:
        return "salir"
    return posiciones[int(posicion_seleccionada) - 1]


def mostrar_jugadores(
    posicion_seleccionada: str, nombre_equipo: str, dataset: list, equipos: dict
) -> list:
    """Muestra los jugadores disponibles para comprar segun la posicion seleccionada
    Ademas llama a la funcion pedir jugadores, si es "salir" retorna "salir" y vuelve al menu
    Si pedir_jugadores devuelve un entero cambia de pagina
    Si  pedir_jugadores devuelve None vuelve a empezar el while
    Si jugadores_seleccionados es valido devuelve jugadores_seleccionados
    -"""
    jugadores_disponibles = filtrar_jugadores_por_posicion(
        posicion_seleccionada, dataset
    )
    pagina_actual = 0
    while True:
        print(HEADER_JUGADORES)
        for i, jugador in enumerate(
            jugadores_disponibles[pagina_actual * 5 : pagina_actual * 5 + 5], start=1
        ):
            print(
                TEMPLATE_JUGADOR_PRECIO.format(
                    n=i, nombre_jugador=jugador[0], precio=jugador[2]
                )
            )
        jugadores_seleccionados = pedir_jugadores(
            jugadores_disponibles,
            pagina_actual,
            nombre_equipo,
            equipos,
        )
        if jugadores_seleccionados is None:
            continue
        if isinstance(jugadores_seleccionados, int):
            pagina_actual = jugadores_seleccionados
            continue
        if jugadores_seleccionados == "salir":
            return "salir"
        return jugadores_seleccionados


# ------------------------------------------------------------------------------------------------


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
        print(
            MSG_COMPRA_EXITOSA.format(
                nombre_jugador=jugador[0],
                nombre_equipo=equipo_seleccionado,
                presupuesto=equipos[equipo_seleccionado]["presupuesto"],
            )
        )
