from constantes import (
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    SALIR,
    ENTRADA_SALIR
)


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
            if opcion_seleccionada == ENTRADA_SALIR:
                return None
            continue
        if int(opcion_seleccionada) < minimo or int(opcion_seleccionada) > maximo:
            print(ERROR_SELECCION_INVALIDA)
            opcion_seleccionada = input("Seleccione una opción: ")
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
    maximo = min(5, len(jugadores_disponibles) - pagina * 5)

    entrada_del_usuario = input(
        "> : Siguiente página\n< : Página anterior\nSeleccione una opcion: "
    )

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

