import pyodbc
import pandas as pd
from cryptography.fernet import Fernet
import json
import warnings

warnings.filterwarnings('ignore')

def cargar_credenciales():
    # Cargar clave
    with open('secret.key', 'rb') as f:
        key = f.read()
    
    cipher = Fernet(key)
    
    # Cargar y desencriptar credenciales
    with open('credenciales.enc', 'rb') as f:
        credenciales_encriptadas = f.read()
    
    credenciales = json.loads(cipher.decrypt(credenciales_encriptadas).decode())
    return credenciales

def ejecutar_sp():
    cred = cargar_credenciales()
    
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={cred['server']};"
        f"DATABASE={cred['database']};"
        f"UID={cred['username']};"
        f"PWD={cred['password']};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=60;"
    )
    
    cursor = conn.cursor()
    cursor.execute("select IDCategoria, cat_abreviatura,cat_descripcion from Categoria where cdn_id = 10 and IDStatus = '71039503-85CF-E511-80C6-000D3A3261F3'")
    
    # Saltar mensajes de error
    while cursor.description is None:
        cursor.nextset()
    
    columnas = [col[0] for col in cursor.description]
    datos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return pd.DataFrame.from_records(datos, columns=columnas)

# Ejecutar
df = ejecutar_sp()
print(df)