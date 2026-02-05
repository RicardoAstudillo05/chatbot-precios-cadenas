# cadenas_config.py

CADENAS_MAPPING = {
    "AMERICAN DELI PATIOS": 2,
    "EL ESPAÑOL": 8,
    "JUAN VALDEZ": 12,
    "BASKIN ROBBINS1": 36,
    "EMBUTSER": 7,
    "KENTUCKY FRENCH CHICKEN": 10,
    "CAFE ASTORIA": 23,
    "FEDERER": 35,
    "MENESTRAS DEL NEGRO": 14,
    "CAJUN": 5,
    "GUS": 9,
    "CASA RES": 25,
    "HELADERIAS KFC": 11,
    "TROPI BURGUER": 16,
    "EL CAPPO": 22,
    "EL CAPPO II": 34,
    "CINNABON": 37,
    "DOLCE INCONTRO": 28
}

CADENAS_LISTA = [
    "AMERICAN DELI PATIOS",
    "EL ESPAÑOL",
    "JUAN VALDEZ",
    "BASKIN ROBBINS1",
    "EMBUTSER",
    "KENTUCKY FRENCH CHICKEN",
    "CAFE ASTORIA",
    "FEDERER",
    "MENESTRAS DEL NEGRO",
    "CAJUN",
    "GUS",
    "CASA RES",
    "HELADERIAS KFC",
    "TROPI BURGUER",
    "EL CAPPO",
    "EL CAPPO II",
    "CINNABON",
    "DOLCE INCONTRO"
]

# Categorías excluidas por cadena (no se incluirán en el reporte)
# Formato: ID de cadena: [lista de IDs de categorías a excluir]
CATEGORIAS_EXCLUIDAS = {
    12: [  # JUAN VALDEZ
        "C2039503-85CF-E511-80C6-000D3A3261F3",
        "43443DC5-97C7-E611-80C6-000D3A330947",
        "0AB705D2-2BE2-E511-80C5-0050568602D0"
    ],
    8: [  # EL ESPAÑOL
        "E0039503-85CF-E511-80C6-000D3A3261F3"
    ],
    10: [  # KENTUCKY FRENCH CHICKEN
        "5CEEC32E-411B-E811-80D1-000D3A019254"
    ]
}

def obtener_cdn_id(nombre_cadena: str) -> int:
    return CADENAS_MAPPING.get(nombre_cadena)

def validar_cadena(nombre_cadena: str) -> bool:
    return nombre_cadena in CADENAS_MAPPING

def obtener_numero_cadena(nombre_cadena: str) -> int:
    try:
        return CADENAS_LISTA.index(nombre_cadena) + 1
    except ValueError:
        return None

def obtener_nombre_por_numero(numero: int) -> str:
    if 1 <= numero <= len(CADENAS_LISTA):
        return CADENAS_LISTA[numero - 1]
    return None

def obtener_categorias_excluidas(cdn_id: int) -> list:
    """Obtiene la lista de categorías excluidas para una cadena específica"""
    return CATEGORIAS_EXCLUIDAS.get(cdn_id, [])