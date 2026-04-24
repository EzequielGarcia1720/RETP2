from funciones_principales import(
    crear_equipos,
    comprar_jugadores,
    vender_jugador,
    ver_plantel,
    armar_alineacion,
    ver_alineacion,
    ver_jugador_mas_utilizado
)
from constantes import (
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    MSG_FIN
)
from data_set import (
    PRESUPUESTO_INICIAL,
    DATASET_JUGADORES
)
def main(datos_jugadores: list, presupuesto_inicial: int):
    """Funcion que despliega el menu principal y llama a las funciones
    correspondientes a cada opcion. Si el usuario ingresa una opcion invalida, se
    le muestra un mensaje de error y se vuelve a desplegar el menu. Si el usuario
    ingresa la opcion de salir, se muestra un mensaje de salida y se termina el programa.
    """
    equipos = {}
    #dataset = procesar_dataset(datos_jugadores)
    dataset = datos_jugadores
    presupuesto = presupuesto_inicial
    menu_principal =(
            "1) Crear equipo\n"
            "2) Comprar jugador\n"
            "3) Vender jugador\n"
            "4) Ver plantel\n"
            "5) Armar alineación\n"
            "6) Ver alineación\n"
            "7) Ver jugador más utilizado\n"
            "8) Salir\n"
            "Ingrese una opción: ")
    while True:
        opcion_seleccionada = input(menu_principal)

        if opcion_seleccionada == "**":
            print(ERROR_INPUT_INVALIDO)
            continue

        acciones = {
            "1": lambda: crear_equipos(equipos, presupuesto),
            "2": lambda: comprar_jugadores(equipos, dataset),
            "3": lambda: vender_jugador(equipos),
            "4": lambda: ver_plantel(equipos),
            "5": lambda: armar_alineacion(equipos),
            "6": lambda: ver_alineacion(equipos),
            "7": lambda: ver_jugador_mas_utilizado(equipos),
            "8": lambda: None,
        }

        if opcion_seleccionada in acciones:
            if opcion_seleccionada == "8":
                print(MSG_FIN)
                return False

            acciones[opcion_seleccionada]()
        else:
            print(ERROR_SELECCION_INVALIDA)

if __name__ == "__main__":
    from data_set import DATASET_JUGADORES, PRESUPUESTO_INICIAL

    main(DATASET_JUGADORES, PRESUPUESTO_INICIAL)
