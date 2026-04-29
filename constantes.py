"""Constantes globales para FundaDT."""

# ----- mensajes generales -----
MSG_FIN = "Finalizando..."

# ----- templates generales -----
HEADER_EQUIPOS = "Equipos disponibles:"
HEADER_JUGADORES = "Jugadores disponibles:"
TEMPLATE_EQUIPO = "{n}. {nombre_equipo}"

# ----- errores generales -----
ERROR_SELECCION_INVALIDA = "Selección inválida"
ERROR_INPUT_INVALIDO = "Formato de entrada inválido"
ERROR_SIN_EQUIPOS = "No existen equipos registrados"

# ----- crear equipo -----
MSG_EQUIPO_CREADO = (
    "El equipo {nombre_equipo} ha sido creado exitosamente con un presupuesto de ${presupuesto}"
)
ERROR_EQUIPO_EXISTENTE = "Ya existe un equipo con ese nombre"
ERROR_FORMATO_NOMBRE = "Formato de nombre de equipo inválido"

# ----- comprar jugador -----
MSG_COMPRA_EXITOSA = (
    "El jugador {nombre_jugador} fue comprado para el equipo {nombre_equipo}. "
    "El nuevo presupuesto del equipo es: ${presupuesto}"
)
TEMPLATE_PRESUPUESTO = "El presupuesto del equipo es ${presupuesto}"
TEMPLATE_JUGADOR_PRECIO = "{n}. {nombre_jugador} - ${precio}"
ERROR_PRESUPUESTO_INSUFICIENTE = "El presupuesto es insuficiente"
ERROR_JUGADOR_EXISTENTE = "El jugador {nombre_jugador} ya se encuentra en el plantel"

# ----- vender jugador -----
TEMPLATE_PLANTEL = """Equipo: {nombre_equipo}
Presupuesto: ${presupuesto}
Plantel:
"""
TEMPLATE_JUGADOR_PLANTEL = "{n}. {nombre_jugador} ({posicion}) [{rol_actual}] - ${precio}"
MSG_PLANTEL_VACIO = "El equipo no posee jugadores"
MSG_VENTA_EXITOSA = (
    "El jugador {nombre_jugador} fue vendido exitosamente. "
    "El nuevo presupuesto del equipo es: ${presupuesto}"
)
MSG_ALINEACION_DESARMADA = "Atención: La alineación del equipo ha sido desarmada"

# ----- ver plantel -----
# usa las mismas que vender jugador

# ----- armar alineación -----
MSG_ALINEACION_GUARDADA = "La nueva alineación del equipo {nombre_equipo} fue guardada exitosamente"
HEADER_ARQUERO = "> ARQUERO:"
HEADER_DEFENSORES = "> DEFENSORES:"
HEADER_MEDIOCAMPISTAS = "> MEDIOCAMPISTAS:"
HEADER_DELANTEROS = "> DELANTEROS:"
HEADER_SUPLENTES = "> SUPLENTES:"
HEADER_TITULARES = "Los jugadores titulares son:"
TEMPLATE_JUGADOR = "{n}. {nombre_jugador}"
TEMPLATE_JUGADOR_POSICION = "{n}. {nombre_jugador} - [{posicion}]"
ERROR_FORMACION_INVALIDA = "Formación inválida"
MSG_CANTIDAD_JUGADORES_INSUFICIENTE = (
    "No hay suficientes jugadores disponibles para armar esta alineación"
)
ERROR_CANTIDAD_INVALIDA = "Para esta posición se necesita(n) {cantidad} jugador(es)"

# ----- ver alineación -----
TEMPLATE_ALINEACION = """La formación es: {formacion}
Los jugadores titulares son:
Delanteros: {delanteros}
Mediocampistas: {mediocampistas}
Defensores: {defensores}
Arquero: {arquero}
Capitán: {capitan}
Los suplentes son:
{suplentes}
"""
MSG_ALINEACION_INEXISTENTE = "El equipo no posee una alineación definida"

# ----- ver jugador más utilizado -----
TEMPLATE_ESTADISTICA_JUGADORES = """Arquero: {arquero}
Defensor: {defensor}
Mediocampista: {mediocampista}
Delantero: {delantero}
"""
MSG_NO_INFORMACION = "No hay información suficiente para mostrar estadísticas"

# ----- constantes de retorno -----
SALIR = "salir"
PEDIR_DE_NUEVO = "pedir de nuevo"
ENTRADA_SALIR = "**"

# ----- Constantes de Inputs ------
INPUT_OPCION = "Seleccione una opción: "
INPUT_NOMBRE_EQUIPO = "Ingrese el nombre de su equipo: "
INPUT_EQUIPO = 'Seleccione un equipo: '
INPUT_FORMACION = 'Ingrese una formación: '
INPUT_COMPRA = "> : Siguiente página\n< : Página anterior\nSeleccione una opcion: "
INPUT_VENTA = "Seleccione el jugador a vender: "
INPUT_JUGADORES_ALINEACION = "Seleccione {cantidad} jugador(es): "
INPUT_CAPITAN_ALINEACION = "Seleccione un capitán: "
INPUT_OPCIONES_POSICIONES = "Posiciones:\n1. Arquero\n2. Defensor\n3. Mediocampista\n4. Delantero\nSeleccione una opcion: "
INPUT_POSICIONES = "Seleccione una posición: "


# ---- Constantes crear_equipo ----
LARGO_MAX_NOMBRE_EQUIPO = 50

# ---- Constantes mostrar_jugadores_compra ----
JUGADORES_POR_PAGINA = 5

# ---- -----
POSICION_ARQUERO = "Arquero"
POSICION_DEFENSOR = "Defensor"
POSICION_MEDIOCAMPISTA = "Mediocampista"
POSICION_DELANTERO = "Delantero"

ROL_SUPLENTE = "Suplente"
ROL_TITULAR = "Titular"
ROL_RESERVA = "Reserva"
ROL_CAPITAN = "Capitan"



# ---- Constantes armar_alineacion ----
MINIMO_JUGADORES_EN_PLANTEL = 16
MINIMO_JUGADORES_EN_FORMACION = 10
ITEM_LISTA_ALINEACION_SUPLENTES = "Suplentes"
ITEM_LISTA_ALINEACION_TITULARES = "Titulares"
ITEM_LISTA_ALINEACION_DEFENSORES = "Defensores"
ITEM_LISTA_ALINEACION_MEDIOCAMPISTAS = "Mediocampistas"
ITEM_LISTA_ALINEACION_DELANTEROS = "Delanteros"
ITEM_LISTA_ALINEACION_ARQUERO = "Arquero"
ITEM_LISTA_ALINEACION_CAPITAN = "Capitan"
