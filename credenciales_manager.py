import json
import logging
from cryptography.fernet import Fernet
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class CredencialesManager:
    
    def __init__(self, key_file: str = 'secret.key', cred_file: str = 'credenciales.enc'):
        self.key_file = key_file
        self.cred_file = cred_file
        self._credenciales = None
    
    def cargar_credenciales(self) -> Optional[Dict]:
        try:
            with open(self.key_file, 'rb') as f:
                key = f.read()
            
            cipher = Fernet(key)
            
            with open(self.cred_file, 'rb') as f:
                credenciales_encriptadas = f.read()
            
            credenciales_json = cipher.decrypt(credenciales_encriptadas).decode()
            self._credenciales = json.loads(credenciales_json)
            
            logger.info("Credenciales cargadas exitosamente")
            return self._credenciales
            
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {e.filename}")
            return None
        except Exception as e:
            logger.error(f"Error al cargar credenciales: {e}")
            return None
    
    def obtener_connection_string(self) -> Optional[str]:
        if self._credenciales is None:
            self.cargar_credenciales()
        
        if self._credenciales is None:
            return None
        
        try:
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self._credenciales['server']};"
                f"DATABASE={self._credenciales['database']};"
                f"UID={self._credenciales['username']};"
                f"PWD={self._credenciales['password']};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
                f"Connection Timeout=60;"
            )
            
            return connection_string
            
        except KeyError as e:
            logger.error(f"Falta credencial requerida: {e}")
            return None
    
    def validar_credenciales(self) -> bool:
        if self._credenciales is None:
            self.cargar_credenciales()
        
        if self._credenciales is None:
            return False
        
        campos_requeridos = ['server', 'database', 'username', 'password']
        
        for campo in campos_requeridos:
            if campo not in self._credenciales:
                logger.error(f"Falta campo requerido: {campo}")
                return False
            
            if not self._credenciales[campo]:
                logger.error(f"Campo vacío: {campo}")
                return False
        
        logger.info("Credenciales validadas correctamente")
        return True

_credenciales_manager = None

def obtener_credenciales_manager() -> CredencialesManager:
    global _credenciales_manager
    
    if _credenciales_manager is None:
        _credenciales_manager = CredencialesManager()
    
    return _credenciales_manager

def cargar_credenciales() -> Optional[Dict]:
    manager = obtener_credenciales_manager()
    return manager.cargar_credenciales()

def obtener_connection_string() -> Optional[str]:
    manager = obtener_credenciales_manager()
    return manager.obtener_connection_string()