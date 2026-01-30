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