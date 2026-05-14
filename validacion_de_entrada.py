# comprar jugador
from constantes import CANTIDAD_VALORES_FORMACION, ERROR_CANTIDAD_INVALIDA, ERROR_FORMACION_INVALIDA, ERROR_INPUT_INVALIDO, ERROR_SELECCION_INVALIDA, MINIMO_JUGADORES_EN_FORMACION, PEDIR_DE_NUEVO
import validaciones
def identificar_entrada(
    entrada_del_usuario: str,
    sel_inv_err_msg: str,
    input_err_msg: str,
    maximo: int,
) -> list | None:
    """Identifica si la entrada del usuario corresponde a una compra individual o multiple.
    - Si es individual y es un entero entre 1 y maximo devuelve una lista con un unico valor.
    - Si es multiple llama a la funcion procesar_multiples, si esta devuelve None la funcion
    devuelve None, sino devuelve una lista de indices, si alguno de esos indices está fuera del
    rango de 1 y maximo devuelve None e imprime sel_inv_err_msg.
    - Si no es ni multiple ni individual imprime sel_inv_err_msg y devuelve None.
   
    """

    es_individual = entrada_del_usuario.lstrip("-").isdigit()
    es_multiple = "-" in entrada_del_usuario
    jugadores_seleccionados = None

    if es_individual:
        jugadores_seleccionados = [entrada_del_usuario]
    elif es_multiple:
        jugadores_seleccionados = validaciones.procesar_multiples(
            entrada_del_usuario, input_err_msg
        )
        if jugadores_seleccionados is None:
            return None
    else:
        print(input_err_msg)
        return None

    if jugadores_seleccionados is None:
        return None
    for indice in jugadores_seleccionados:
        if int(indice) > maximo or int(indice) < 1:
            print(sel_inv_err_msg)
            return None

    return jugadores_seleccionados


def procesar_formacion(formacion_seleccionada: str) -> str | list:
    """Recibe la entrada del usuario, la "splitea" y devuelve la lista creada
    - Si len(lista) es distinto a CANTIDAD_VALORES_FORMACION devuelve PEDIR_DE_NUEVO
    e imprime ERROR_FORMACION_INVALIDA
    - Si no cumple el formato devuelve PEDIR_DE_NUEVO e imprime ERROR_INPUT_INVALIDO
    """
    if formacion_seleccionada.strip() == "" or formacion_seleccionada.count("-") != 2:
        print(ERROR_INPUT_INVALIDO)
        return PEDIR_DE_NUEVO
    lista_formacion = formacion_seleccionada.split("-")
    if len(lista_formacion) != CANTIDAD_VALORES_FORMACION:
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
    if suma != MINIMO_JUGADORES_EN_FORMACION:
        print(ERROR_FORMACION_INVALIDA)
        return PEDIR_DE_NUEVO

    return lista_formacion

def procesar_multiples(
    entrada_del_usuario: str, lista_filtrada: list, cantidad_de_jugadores: int
) -> list | None:
    """Recibe la entrada del usuario de jugadores multiples y verifica
    1. Que no sean duplicados -> sino imprime ERROR_INPUT_INVALIDO y devuelve None
    2. Que todos sean numeros -> sino imprime ERROR_INPUT_INVALIDO y devuelve None
    3. Que la cantidad de jugadores seleccionados no sea distinta a cantidad_de_jugadores ->
    sino imprime ERROR_CANTIDAD_INVALIDA y devuelve None
    4. Que los índices ingresados estén dentro del rango de la lista_filtrada
        -> sino imprime ERROR_SELECCION_INVALIDA y devuelve None
    De ser válida devuelve una lista con los diccionarios de los jugadores seleccionados.

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
