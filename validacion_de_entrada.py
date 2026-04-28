# comprar jugador
import validaciones
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

    if es_individual:
        jugadores_seleccionados = [entrada_del_usuario]
    elif es_multiple:
        jugadores_seleccionados = validaciones.procesar_multiples(
            entrada_del_usuario, input_err_msg
        )
        if jugadores_seleccionados is None:
            return None
    else:
        print(sel_inv_err_msg)

    if jugadores_seleccionados is None:
        return None
    for indice in jugadores_seleccionados:
        if int(indice) > maximo or int(indice) < 1:
            print(sel_inv_err_msg)
            return None

    return jugadores_seleccionados
