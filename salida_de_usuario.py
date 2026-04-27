# Comprar jugadores
from constantes import (
    ERROR_SIN_EQUIPOS,
    HEADER_ARQUERO,
    HEADER_DEFENSORES,
    HEADER_DELANTEROS,
    HEADER_EQUIPOS,
    HEADER_JUGADORES,
    HEADER_MEDIOCAMPISTAS,
    HEADER_SUPLENTES,
    HEADER_TITULARES,
    MSG_ALINEACION_INEXISTENTE,
    MSG_COMPRA_EXITOSA,
    MSG_PLANTEL_VACIO,
    SALIR,
    TEMPLATE_ALINEACION,
    TEMPLATE_EQUIPO,
    TEMPLATE_JUGADOR,
    TEMPLATE_JUGADOR_PLANTEL,
    TEMPLATE_JUGADOR_POSICION,
    TEMPLATE_JUGADOR_PRECIO,
    TEMPLATE_PLANTEL,
    TEMPLATE_PRESUPUESTO,
    INPUT_EQUIPO,
    INPUT_POSICIONES
)
import entrada_de_usuario
import validaciones
import manejo_de_alineaciones
import manejo_de_equipos


def mostrar_equipos(equipos: dict) -> str:
    """Muestra los equipos disponibles para comprar jugadores y llama la
    funcion pedir_entero para que el usuario seleccione un equipo
    - Si equipo seleccionado es None devuelve "salir"
    - Si no hay equipos disponibles imprime ERROR_SIN_EQUIPOS y retorna "salir"
    - Si equipo seleccionado es valido devuelve el nombre del equipo
    """
    if not equipos:
        print(ERROR_SIN_EQUIPOS)
        return SALIR
    opciones = sorted(list(equipos))
    maximo = len(opciones)
    mensaje = HEADER_EQUIPOS
    for indice, opcion in enumerate(opciones, start=1):
        mensaje += "\n" + TEMPLATE_EQUIPO.format(n=indice, nombre_equipo=opcion)
    print(mensaje)
    equipo_seleccionado = entrada_de_usuario.pedir_entero(INPUT_EQUIPO, 1, maximo)
    if equipo_seleccionado is None:
        return SALIR
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
    posicion_seleccionada = entrada_de_usuario.pedir_entero(
        INPUT_POSICIONES, 1, len(posiciones)
    )
    if posicion_seleccionada is None:
        return SALIR
    return posiciones[int(posicion_seleccionada) - 1]


def mostrar_jugadores_compra(
    posicion_seleccionada: str, nombre_equipo: str, dataset: dict, equipos: dict
) -> list:
    """Muestra los jugadores disponibles para comprar segun la posicion seleccionada
    Ademas llama a la funcion pedir jugadores, si es "salir" retorna "salir" y vuelve al menu
    Si pedir_jugadores devuelve un entero cambia de pagina
    Si  pedir_jugadores devuelve None vuelve a empezar el while
    Si jugadores_seleccionados es valido devuelve jugadores_seleccionados
    -"""
    jugadores_disponibles = dataset[posicion_seleccionada]
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
        jugadores_seleccionados = entrada_de_usuario.pedir_jugadores(
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
        if jugadores_seleccionados == SALIR:
            return SALIR
        return jugadores_seleccionados

def imprimir_mensaje_compra(nombre_jugador, equipo_seleccionado, presupuesto_equipo):
    print(
        MSG_COMPRA_EXITOSA.format(
            nombre_jugador=nombre_jugador,
            nombre_equipo=equipo_seleccionado,
            presupuesto=presupuesto_equipo,
        )
    )

# Vender


def mostrar_plantel_venta(equipo: str, equipos: dict) -> str | None | tuple:
    """Funcion que muestra los jugadores del plantel y llama a la funcion pedir_entrada.
    Recibe el equipo seleccionado y el diccionario de equipos.
    - Si el equipo seleccionado no tiene jugadores vuelve al menu
    principal e imprime MSG_PLANTEL_VACIO
    - Si pedir_entrada devuelve "salir" devuelve "salir" y vuelve al menu principal
    - Si pedir_entrada devuelve None vuelve a empezar el while solicitando entrada
    nuevamente.
    - Si la entrada es valida devuelve la tupla del jugador a vender.

    """
    if mostrar_plantel(equipo, equipos) == SALIR:
        return SALIR
    plantel_ordenado = manejo_de_equipos.ordenar_jugadores(equipos, equipo)
    while True:
        jugador_a_vender = entrada_de_usuario.pedir_entrada(plantel_ordenado)
        if jugador_a_vender == SALIR:
            return SALIR
        if jugador_a_vender is None:
            continue
        jugador_a_vender = plantel_ordenado[int(jugador_a_vender) - 1]

        return jugador_a_vender


def mostrar_plantel(equipo: str, equipos: dict):
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
    if not validaciones.tiene_jugadores(equipo, equipos):
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
    plantel_ordenado = manejo_de_equipos.ordenar_jugadores(equipos, equipo)
    for jugador in plantel_ordenado:
        rol_actual = casos_de_rol.get(
            (
                validaciones.es_titular(jugador, equipo, equipos),
                validaciones.es_suplente(jugador, equipo, equipos),
            )
        )()
        mensaje += TEMPLATE_JUGADOR_PLANTEL.format(
            n=contador,
            nombre_jugador=jugador['nombre'],
            posicion=jugador['posicion'],
            rol_actual=rol_actual,
            precio=jugador['precio'],
        )
        if contador < len(plantel_ordenado):
            mensaje += "\n"
        contador += 1
    print(mensaje)
    return True


# Armar alineacion


def imprimir_lista_jugadores(header: str, lista_filtrada: list):
    """
    Recibe el HEADER y la lista filtrada de jugadores segun la posicion y la imprime
    """
    mensaje = header
    if header in (HEADER_SUPLENTES, HEADER_TITULARES):
        for indice, jugador in enumerate(lista_filtrada):
            mensaje += "\n" + TEMPLATE_JUGADOR_POSICION.format(
                n=indice + 1,
                nombre_jugador=jugador['nombre'],
                posicion=jugador['posicion'],
            )
    else:
        for indice, jugador in enumerate(lista_filtrada):
            mensaje += "\n" + TEMPLATE_JUGADOR.format(
                n=indice + 1,
                nombre_jugador=jugador['nombre'],
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

    alineacion = {}

    for posicion, header, clave_dict in [
        ("Arquero", HEADER_ARQUERO, "Arquero"),
        ("Defensor", HEADER_DEFENSORES, "Defensores"),
        ("Mediocampista", HEADER_MEDIOCAMPISTAS, "Mediocampistas"),
        ("Delantero", HEADER_DELANTEROS, "Delanteros"),
        ("Suplente", HEADER_SUPLENTES, "Suplentes"),
        ("Capitan", HEADER_TITULARES, "Capitan"),
    ]:
        jugadores_ya_elegidos = manejo_de_alineaciones.obtener_jugadores_ya_elegidos(
            alineacion
        )
        plantel = manejo_de_equipos.ordenar_jugadores(equipos, equipo)
        listas_filtradas = {
            "Suplente": sorted(
                [
                    jugador
                    for jugador in plantel
                    if jugador not in jugadores_ya_elegidos
                ], key=lambda x: x['nombre']
            ),
            "Capitan": sorted(
                [
                    jugador
                    for jugador in plantel
                    if jugador in jugadores_ya_elegidos
                    and jugador not in alineacion.get("Suplentes", [])
                ], key=lambda x: x['nombre']
            ),
        }
        lista_filtrada = listas_filtradas.get(
            posicion,
            sorted(
                [
                    jugador
                    for jugador in plantel
                    if jugador['posicion'] == posicion
                ],
                key=lambda x: x['nombre'],
            ),
        )
        imprimir_lista_jugadores(header, lista_filtrada)

        jugadores_seleccionados = manejo_de_alineaciones.obtener_seleccion_posicion(
            posicion, lista_filtrada, formacion_seleccionada
        )

        if jugadores_seleccionados == 'salir':
            return SALIR

        alineacion[clave_dict] = jugadores_seleccionados

    lista_titulares = []

    for clave in ["Arquero", "Defensores", "Mediocampistas", "Delanteros"]:
        if isinstance(alineacion[clave], list):
            lista_titulares.extend(alineacion[clave])
        else:
            lista_titulares.append(alineacion[clave])

    alineacion["Titulares"] = lista_titulares
    return alineacion


def mostrar_alineacion(equipo: str, equipos: dict) -> str:
    """Crea el mensaje con la alineacion del equipo seleccionado.
    - Si el equipo no tiene alineacion imprime MSG_ALINEACION_INEXISTENTE y devuelve "salir"
    Devuelve el mensaje con la alineacion del equipo seleccionado
    """
    if validaciones.alineacion_inexistente(equipos, equipo):
        print(MSG_ALINEACION_INEXISTENTE)
        return SALIR
    formacion = "-".join(manejo_de_alineaciones.adquirir_formacion(equipos, equipo))
    defensores, mediocampistas, delanteros, arquero, suplentes_sin_formato, capitan = (
        manejo_de_alineaciones.adquirir_todas_las_posiciones(equipos, equipo)
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
                n=indice, nombre_jugador=jugador['nombre'], posicion=jugador['posicion']
            )
            for indice, jugador in enumerate(suplentes_sin_formato, start=1)
        ),
    ).rstrip("\n")
    return mensaje
