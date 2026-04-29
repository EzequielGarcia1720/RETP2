# comprar jugador
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
