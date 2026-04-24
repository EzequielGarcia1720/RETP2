from constantes import (
    HEADER_ARQUERO,
    HEADER_DEFENSORES,
    HEADER_MEDIOCAMPISTAS,
    HEADER_DELANTEROS,
    HEADER_SUPLENTES,
    HEADER_TITULARES,
    TEMPLATE_JUGADOR,
    TEMPLATE_JUGADOR_POSICION,
    ERROR_CANTIDAD_INVALIDA,
    ERROR_INPUT_INVALIDO,
    ERROR_FORMACION_INVALIDA,
    ERROR_SELECCION_INVALIDA,
    MSG_CANTIDAD_JUGADORES_INSUFICIENTE,
    SALIR,
    PEDIR_DE_NUEVO,
)

# ---------------------- Verificaciones ----------------


def verificar_cant_jugadores(equipo: str, equipos: dict, formacion_seleccionada: list)-> bool:
    """Recibe el equipo seleccionado, el diccionario de equipos y la lista con la formacion
    seleccionada.
    - Si la cantidad de jugadores en el plantel es menor a 16 devuelve False
    - Si no hay jugadores suficientes para la formacion seleccionada devuelve False
    - Sino devuelve True
    """
    if len(equipos[equipo]["plantel"]) < 16:
        print(MSG_CANTIDAD_JUGADORES_INSUFICIENTE)
        return False
    arqueros = 0
    defensores = 0
    mediocampistas = 0
    delanteros = 0
    for jugador in equipos[equipo]["plantel"]:
        if jugador[1] == "Arquero":
            arqueros += 1
        if jugador[1] == "Defensor":
            defensores += 1
        if jugador[1] == "Mediocampista":
            mediocampistas += 1
        if jugador[1] == "Delantero":
            delanteros += 1
    if (
        arqueros < 1
        or defensores < int(formacion_seleccionada[0])
        or mediocampistas < int(formacion_seleccionada[1])
        or delanteros < int(formacion_seleccionada[2])
    ):
        print(MSG_CANTIDAD_JUGADORES_INSUFICIENTE)
        return False
    return True


def procesar_formacion(formacion_seleccionada: str):
    """Recibe la entrada del usuario, la "splitea" y devuelve la lista creada
    - Si len(lista) es distinto a 3 retorna "pedir de nuevo" e imprime ERROR_FORMACION_INVALIDA
    - Si no cumple el formato devuelve "pedir de nuevo" e imprime ERROR_INPUT_INVALIDO
    """
    if formacion_seleccionada.strip() == "" or formacion_seleccionada.count("-") != 2:
        print(ERROR_INPUT_INVALIDO)
        return PEDIR_DE_NUEVO
    lista_formacion = formacion_seleccionada.split("-")
    if len(lista_formacion) != 3:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO
    suma = 0
    for jugadores_posicion in lista_formacion:
        if not jugadores_posicion.isdigit():
            print(ERROR_INPUT_INVALIDO)
            return PEDIR_DE_NUEVO
        if int(jugadores_posicion) == 0:
            print(ERROR_FORMACION_INVALIDA)
            return PEDIR_DE_NUEVO
        suma += int(jugadores_posicion)
    if suma != 10:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO

    return lista_formacion


def procesar_multiples(
    entrada_del_usuario: str, lista_filtrada: list, cantidad_de_jugadores: int
) -> list | None:
    """Recibe la entrada del usuario de jugadores multiples y verifica
    1. Que no sean duplicados
    2. Que todos sean numeros
    
    """
    jugadores_seleccionados = entrada_del_usuario.split("-")

    son_numeros = all(jugador.isdigit() for jugador in jugadores_seleccionados)
    if not son_numeros:
        print(ERROR_INPUT_INVALIDO)
        return None

    sin_duplicados = len(jugadores_seleccionados) == len(set(jugadores_seleccionados))
    if not sin_duplicados:
        print(ERROR_INPUT_INVALIDO)
        return None

    if len(jugadores_seleccionados) != int(cantidad_de_jugadores):
        print(ERROR_CANTIDAD_INVALIDA.format(cantidad=cantidad_de_jugadores))
        return None
    lista_jugadores = []
    for indice in jugadores_seleccionados:
        if int(indice) > len(lista_filtrada):
            print(ERROR_SELECCION_INVALIDA)
            return None
        lista_jugadores.append(lista_filtrada[int(indice) - 1])

    return lista_jugadores


# -------------------- Inputs ---------------------


def pedir_formacion(equipo: str, equipos: dict) -> list | str | None:
    """Pide al usuario entrada de una formacion, esta debe
    ser del formato X-Y-Z siendo la suma X Y Z = 10
    - Si la entrada es "**" devuelve salir
    - Si formacion seleccionada es "pedir de nuevo" reinicia el while
    Si la formacion es valida llama a la funcion verificar_cant_jugadores, si esta devuelve
    False vuelve al menu principal, sino devuelve una lista con la formacion seleccionada
    """
    while True:
        formacion_seleccionada = input("Ingrese una formación: ")
        if formacion_seleccionada == "**":
            return SALIR
        formacion_seleccionada = procesar_formacion(formacion_seleccionada)
        if formacion_seleccionada == "pedir de nuevo":
            continue
        if verificar_cant_jugadores(equipo, equipos, formacion_seleccionada):
            return formacion_seleccionada
        return SALIR


def pedir_jugadores(
    formacion_seleccionada: list, posicion: str, lista_filtrada: list
) -> list | str | None:
    """Pide al usuario que ingrese una cantidad de jugadores de una lista numerada.
    - Los jugadores deben estar separados por guiones y estos deben ser cuantos se
    hayan especificado en la formacion seleccionada (a excepcion del arquero, suplentes
    y el capitan que son siempre 1, 5 y 1)
    - Si la entrada es "**" devuelve "salir" y vuelve al menu principal
    - Si la entrada no es un numero imprime ERROR_INPUT_INVALIDO y devuelve None
    - Si la entrada es menor a 1 o mayor a la cantidad de jugadores en la lista filtrada
    imprime ERROR_SELECCION_INVALIDA y devuelve None
    - Si la entrada es valida:
        - Si es de seleccion multiple la procesa y se devuelve jugadores_seleccionados
        - Si es de seleccion indivual se asigna y devuelve jugadores_seleccionados
    """

    cantidades = {
        "Arquero": 1,
        "Suplente": 5,
        "Capitan": 1,
        "Defensor": formacion_seleccionada[0],
        "Mediocampista": formacion_seleccionada[1],
        "Delantero": formacion_seleccionada[2],
    }

    cantidad = cantidades.get(posicion)
    if posicion != "Capitan":
        entrada_del_usuario = input(f"Seleccione {cantidad} jugador(es): ")
    else:
        entrada_del_usuario = input("Seleccione un capitán: ")
    if entrada_del_usuario == "**":
        return SALIR

    jugadores_seleccionados = None

    if posicion in {"Arquero", "Capitan"}:
        if entrada_del_usuario.lstrip("-").isdigit():
            indice = int(entrada_del_usuario) - 1
            if 0 <= indice < len(lista_filtrada):
                jugadores_seleccionados = lista_filtrada[indice]
            else:
                print(ERROR_SELECCION_INVALIDA)
        else:
            print(ERROR_INPUT_INVALIDO)
    else:
        jugadores_seleccionados = procesar_multiples(
            entrada_del_usuario, lista_filtrada, cantidad
        )
        if jugadores_seleccionados is None:
            return None
    return jugadores_seleccionados


# ---------------------  --------------------------


def obtener_seleccion_posicion(
    posicion: str, lista_filtrada: list, formacion: list
) -> list:
    """
    Recibe el nombre de la posicion, la lista filtrada segun esa posicion y la formacion como lista
    y llama a la funcion pedir_jugadores.
    - Si esta devuelve "salir" devuelve "salir" y se vuelve al menu principal
    - Sino devuelve una lista con los jugadores seleccionados
    """
    while True:
        jugadores = pedir_jugadores(formacion, posicion, lista_filtrada)
        if jugadores == SALIR:
            return SALIR
        if jugadores:
            return jugadores


def obtener_jugadores_ya_elegidos(alineacion: dict) -> list:
    """
    Recibe el diccionario de la alineacion y devuelve una lista con los jugadores ya elegidos
    """
    elegidos = []
    for valor_posicion in alineacion.values():
        if isinstance(valor_posicion, list):
            elegidos.extend(valor_posicion)
        else:
            elegidos.append(valor_posicion)
    return elegidos


# ---------------- Outputs -----------------------


def imprimir_lista_jugadores(header: str, lista_filtrada: list):
    """
    Recibe el HEADER y la lista filtrada de jugadores segun la posicion y la imprime
    """
    mensaje = header
    if header in (HEADER_SUPLENTES, HEADER_TITULARES):
        for indice, jugador in enumerate(lista_filtrada):
            mensaje += "\n" + TEMPLATE_JUGADOR_POSICION.format(
                n=indice + 1,
                nombre_jugador=jugador[0],
                posicion=jugador[1],
            )
#    elif header == HEADER_TITULARES:
#        for indice, jugador in enumerate(lista_filtrada):
#            mensaje += "\n" + TEMPLATE_JUGADOR_POSICION.format(
#                n=indice + 1,
#                nombre_jugador=jugador[0],
#                posicion=jugador[1],
#            )
    else:
        for indice, jugador in enumerate(lista_filtrada):
            mensaje += "\n" + TEMPLATE_JUGADOR.format(
                n=indice + 1,
                nombre_jugador=jugador[0],
            )
    print(mensaje)


def mostrar_jugadores(equipos: dict, equipo: str, formacion_seleccionada: list):
    """Muestra la lista de jugadores segun la posicion y llama a la funcion pedir_jugadores
    para que el usuario ingrese los indices de los jugadores de la lista que desea agregar a
    la alineacion en esa posicion.
    - Si jugadores_seleccionados es "salir" devuelve "salir" y vuelve al menu principal
    - Si jugadores_seleccionados es valido se agregan los jugadores a la alineacion
    Una vez ingresados todos los jugadores devuelve alineacion
    """

    # (Posicion en la tupla del jugador, el header a imprimir, la clave que irá en el diccionario)
    config_posiciones = [
        ("Arquero", HEADER_ARQUERO, "Arquero"),
        ("Defensor", HEADER_DEFENSORES, "Defensores"),
        ("Mediocampista", HEADER_MEDIOCAMPISTAS, "Mediocampistas"),
        ("Delantero", HEADER_DELANTEROS, "Delanteros"),
        ("Suplente", HEADER_SUPLENTES, "Suplentes"),
        ("Capitan", HEADER_TITULARES, "Capitan"),
    ]

    alineacion = {}

    for posicion, header, clave_dict in config_posiciones:
        jugadores_ya_elegidos = obtener_jugadores_ya_elegidos(alineacion)
        if posicion == "Suplente":

            lista_filtrada = sorted(
                [
                    jugador
                    for jugador in equipos[equipo]["plantel"]
                    if jugador not in jugadores_ya_elegidos
                ]
            )
        elif posicion == "Capitan":
            lista_filtrada = sorted(
                [
                    jugador
                    for jugador in equipos[equipo]["plantel"]
                    if jugador in jugadores_ya_elegidos
                    and jugador not in alineacion.get("Suplentes", [])
                ]
            )
        else:
            lista_filtrada = sorted(
                [
                    jugador
                    for jugador in equipos[equipo]["plantel"]
                    if jugador[1] == posicion
                ]
            )
        # Creo que podria haber hecho un diccionario pero me acabo de dar cuenta y ya es tarde

        imprimir_lista_jugadores(header, lista_filtrada)

        jugadores_seleccionados = obtener_seleccion_posicion(
            posicion, lista_filtrada, formacion_seleccionada
        )

        if jugadores_seleccionados == SALIR:
            return SALIR

        alineacion[clave_dict] = jugadores_seleccionados

    claves_titulares = ["Arquero", "Defensores", "Mediocampistas", "Delanteros"]
    lista_titulares = []

    for clave in claves_titulares:
        valor_posicion = alineacion[clave]
        if isinstance(valor_posicion, list):
            lista_titulares.extend(valor_posicion)
        else:
            lista_titulares.append(valor_posicion)

    alineacion["Titulares"] = lista_titulares
    return alineacion
