from constantes import (
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    JUGADORES_POR_PAGINA,
    ARQUERO,
    DEFENSOR,
    DELANTERO,
    MEDIOCAMPISTA,
    ROL_CAPITAN,
    ROL_SUPLENTE,
    SALIR,
    ENTRADA_SALIR,
    INPUT_FORMACION,
    INPUT_OPCION,
    INPUT_COMPRA,
    INPUT_VENTA,
    INPUT_JUGADORES_ALINEACION,
    INPUT_CAPITAN_ALINEACION,
)
import validacion_de_entrada
import validaciones
import manejo_de_alineaciones

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
    if opcion_seleccionada == ENTRADA_SALIR:
        return None

    while True:
        if not opcion_seleccionada.isdigit():
            print(ERROR_INPUT_INVALIDO)
            opcion_seleccionada = input(INPUT_OPCION)
            if opcion_seleccionada == ENTRADA_SALIR:
                return None
            continue
        if int(opcion_seleccionada) < minimo or int(opcion_seleccionada) > maximo:
            print(ERROR_SELECCION_INVALIDA)
            opcion_seleccionada = input(INPUT_OPCION)
            if opcion_seleccionada == ENTRADA_SALIR:
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
    maximo = min(JUGADORES_POR_PAGINA, len(jugadores_disponibles) - pagina * JUGADORES_POR_PAGINA)

    entrada_del_usuario = input(INPUT_COMPRA)

    while True:
        match entrada_del_usuario:
            case "**":
                resultado_a_devolver = SALIR
                break

            case "<":
                if pagina > 0:
                    resultado_a_devolver = pagina - 1
                    break

                print(ERROR_SELECCION_INVALIDA)
                entrada_del_usuario = input(INPUT_OPCION)
                continue

            case ">":
                if (pagina + 1) * JUGADORES_POR_PAGINA < len(jugadores_disponibles):
                    resultado_a_devolver = pagina + 1
                    break

                print(ERROR_SELECCION_INVALIDA)
                entrada_del_usuario = input(INPUT_OPCION)
                continue

            case _:
                indices_de_jugadores = validacion_de_entrada.identificar_entrada(
                    entrada_del_usuario,
                    ERROR_SELECCION_INVALIDA,
                    ERROR_INPUT_INVALIDO,
                    maximo,
                )

                if not indices_de_jugadores:
                    entrada_del_usuario = input(INPUT_OPCION)
                    continue

                lista_jugadores = []
                for indice in indices_de_jugadores:
                    indice_real = (pagina_actual * JUGADORES_POR_PAGINA) + int(indice) - 1
                    lista_jugadores.append(jugadores_disponibles[indice_real])
                if not validaciones.verificar_existencia_jugador(
                    lista_jugadores, nombre_equipo, equipos
                ):
                    entrada_del_usuario = input(INPUT_OPCION)
                    continue

                resultado_a_devolver = lista_jugadores
                break
    return resultado_a_devolver

# Vender

def pedir_entrada(plantel_ordenado)-> str | None:
    """Funcion que pide la entrada del jugador a vender.
    - Si la entrada es "**" devuelve "salir" y vuelve al menu principal
    - Si la entrada no es un numero imprime ERROR_INPUT_INVALIDO y devuelve None
    - Si la entrada es menor a 1 o mayor a la cantidad de jugadores en el plantel
    imprime ERROR_SELECCION_INVALIDA y devuelve None
    - Si la entrada es valida devuelve la entrada del usuario
    """
    entrada_del_usuario = input(INPUT_VENTA)
    if entrada_del_usuario == ENTRADA_SALIR:
        return SALIR
    if not entrada_del_usuario.isdigit():
        print(ERROR_INPUT_INVALIDO)
        return None
    if int(entrada_del_usuario) < 1 or int(entrada_del_usuario) > len(
        plantel_ordenado
    ):
        print(ERROR_SELECCION_INVALIDA)
        return None
    return entrada_del_usuario

# Armar alineacion

def pedir_formacion(equipo: str, equipos: dict) -> list | str | None:
    """Pide al usuario entrada de una formacion, esta debe
    ser del formato X-Y-Z siendo la suma X Y Z = 10
    - Si la entrada es "**" devuelve salir
    - Si formacion seleccionada es "pedir de nuevo" reinicia el while
    Si la formacion es valida llama a la funcion verificar_cant_jugadores, si esta devuelve
    False vuelve al menu principal, sino devuelve una lista con la formacion seleccionada
    """
    while True:
        formacion_seleccionada = input(INPUT_FORMACION)
        if formacion_seleccionada == ENTRADA_SALIR:
            return SALIR
        formacion_seleccionada = manejo_de_alineaciones.procesar_formacion(formacion_seleccionada)
        if formacion_seleccionada == "pedir de nuevo":
            continue
        if validaciones.verificar_cant_jugadores(equipo, equipos, formacion_seleccionada):
            return formacion_seleccionada
        return SALIR


def pedir_jugadores_alineacion(
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
        ARQUERO: 1,
        ROL_SUPLENTE: 5,
        ROL_CAPITAN: 1,
        DEFENSOR: formacion_seleccionada[0],
        MEDIOCAMPISTA: formacion_seleccionada[1],
        DELANTERO: formacion_seleccionada[2],
    }

    cantidad = cantidades.get(posicion)
    if posicion != ROL_CAPITAN:
        entrada_del_usuario = input(INPUT_JUGADORES_ALINEACION.format(cantidad=cantidad))
    else:
        entrada_del_usuario = input(INPUT_CAPITAN_ALINEACION)
    if entrada_del_usuario == ENTRADA_SALIR:
        return SALIR

    jugadores_seleccionados = None

    if posicion in [ARQUERO, ROL_CAPITAN]:
        if entrada_del_usuario.lstrip("-").isdigit():
            indice = int(entrada_del_usuario) - 1
            if 0 <= indice < len(lista_filtrada):
                jugadores_seleccionados = lista_filtrada[indice]
            else:
                print(ERROR_SELECCION_INVALIDA)
        else:
            print(ERROR_INPUT_INVALIDO)
    else:
        jugadores_seleccionados = manejo_de_alineaciones.procesar_multiples(
            entrada_del_usuario, lista_filtrada, cantidad
        )
        if jugadores_seleccionados is None:
            return None
    return jugadores_seleccionados
