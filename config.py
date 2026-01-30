import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', './descargas')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', '120'))
    
    @classmethod
    def validar(cls):
        errores = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errores.append("TELEGRAM_BOT_TOKEN no está configurado en .env")
        
        if errores:
            print("\n".join(errores))
            return False
        
        return True