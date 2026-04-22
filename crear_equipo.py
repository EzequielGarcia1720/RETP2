"""Importo las constantes"""


def validar_formato_equipo(nombre_equipo):
    """Funcion que valida el nombre del equipo ingresado. El nombre no debe contener numeros,
    caracteres especiales, exceder los 50 caracteres ni ser una cadena vacia. Si el nombre es
    valido, se retorna True, de lo contrario se retorna False."""
    if (
        len(nombre_equipo) > 50
        or len(nombre_equipo) == 0
        or nombre_equipo == ""
        or nombre_equipo.isdigit()
        or nombre_equipo.rstrip() == ""
    ):
        return False
    for caracter in nombre_equipo:
        if not caracter.isalpha() and not caracter.isspace():
            return False
    return True


def existe_equipo(nombre_equipo, equipos):
    """Funcion que verifica si el equipo ya existe.
    Si el equipo existe, se retorna True, de lo contrario se retorna False."""
    return nombre_equipo in equipos
