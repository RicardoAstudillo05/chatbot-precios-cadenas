import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """Clase de configuración centralizada"""
    
    # Configuración de Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Configuración del Sistema
    SISTEMA_URL = os.getenv('SISTEMA_URL', 'https://tudominio.com/login')
    SISTEMA_USUARIO = os.getenv('SISTEMA_USUARIO', 'usuario')
    SISTEMA_PASSWORD = os.getenv('SISTEMA_PASSWORD', 'password')
    
    # Directorios
    DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', './descargas')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Control de acceso
    USUARIOS_AUTORIZADOS = [
        int(uid) for uid in os.getenv('USUARIOS_AUTORIZADOS', '').split(',') 
        if uid.strip()
    ]
    
    @classmethod
    def validar(cls):
        """Valida que todas las configuraciones necesarias estén presentes"""
        errores = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errores.append("❌ TELEGRAM_BOT_TOKEN no está configurado en .env")
        
        if errores:
            print("\n".join(errores))
            return False
        
        return True


# Listado de cadenas
CADENAS = [
    "AMERICAN DELI PATIOS", 
    "EL ESPAÑOL", 
    "JUAN VALDEZ",
    "BASKIN ROBBINS 1", 
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


def obtener_cadenas():
    """Retorna la lista de cadenas disponibles"""
    return CADENAS