from constantes import (
    ERROR_INPUT_INVALIDO,
    ERROR_SELECCION_INVALIDA,
    MSG_FIN,
    ENTRADA_SALIR
)
import funciones_principales

def procesar_dataset(dataset)-> dict:
    """
    Procesa el dataset de forma que los jugadores estén divididos por posición, devolviendo
    dataset_procesado que seria algo como esto:
        dataset_procesado = {
            "Arquero": [jugador1, jugador2, ...],
            "Defensor": [jugador1, jugador2, ...],
            "Mediocampista": [jugador1, jugador2, ...],
            "Delantero": [jugador1, jugador2, ...],
        }
    Cada jugador tiene el siguiente formato:
        (nombre, posición, precio)
    """
    dataset_procesado = {}
    for jugador in dataset:
        posicion = jugador[1]
        if posicion not in dataset_procesado:
            dataset_procesado[posicion] = []
        dataset_procesado[posicion].append(jugador)
    return dataset_procesado

equipos = {}
def main(datos_jugadores: list, presupuesto_inicial: int):
    """Funcion que despliega el menu principal y llama a las funciones
    correspondientes a cada opcion. Si el usuario ingresa una opcion invalida, se
    le muestra un mensaje de error y se vuelve a desplegar el menu. Si el usuario
    ingresa la opcion de salir, se muestra un mensaje de salida y se termina el programa.
    """
    dataset = procesar_dataset(datos_jugadores)
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

        if opcion_seleccionada == ENTRADA_SALIR:
            print(ERROR_INPUT_INVALIDO)
            continue

        acciones = {
            "1": lambda: funciones_principales.crear_equipos(equipos, presupuesto),
            "2": lambda: funciones_principales.comprar_jugadores(equipos, dataset),
            "3": lambda: funciones_principales.vender_jugador(equipos),
            "4": lambda: funciones_principales.ver_plantel(equipos),
            "5": lambda: funciones_principales.armar_alineacion(equipos),
            "6": lambda: funciones_principales.ver_alineacion(equipos),
            "7": lambda: funciones_principales.ver_jugador_mas_utilizado(equipos),
            "8": lambda: None,
        }

        if opcion_seleccionada in acciones:
            if opcion_seleccionada == "8":
                print(MSG_FIN)
                return False

            acciones[opcion_seleccionada]()
        elif opcion_seleccionada.isalpha():
            print(ERROR_INPUT_INVALIDO)
        else:
            print(ERROR_SELECCION_INVALIDA)

if __name__ == "__main__":
    from data_set import DATASET_JUGADORES, PRESUPUESTO_INICIAL

    main(DATASET_JUGADORES, PRESUPUESTO_INICIAL)
