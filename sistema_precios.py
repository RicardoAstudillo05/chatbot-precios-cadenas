import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

logger = logging.getLogger(__name__)


class SistemaPrecios:
    """
    Clase para automatizar la extracción de archivos XLS del sistema de precios
    usando Selenium
    """
    
    def __init__(self):
        """Inicializa el sistema de precios"""
        self.url = Config.SISTEMA_URL
        self.usuario = Config.SISTEMA_USUARIO
        self.password = Config.SISTEMA_PASSWORD
        self.download_dir = os.path.abspath(Config.DOWNLOAD_DIR)
        self.driver = None
        
        # Crear directorio de descargas si no existe
        os.makedirs(self.download_dir, exist_ok=True)
        logger.info(f"Directorio de descargas: {self.download_dir}")
    
    def _configurar_driver(self):
        """Configura y retorna el WebDriver de Chrome con opciones de descarga"""
        chrome_options = Options()
        
        # Configuraciones para descargas automáticas
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Ejecutar en modo headless (sin ventana visible)
        # COMENTA ESTA LÍNEA SI QUIERES VER EL NAVEGADOR DURANTE PRUEBAS
        # chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        return driver
    
    def login(self):
        """
        Realiza el login al sistema
        
        Returns:
            bool: True si el login fue exitoso, False en caso contrario
        """
        try:
            logger.info("=== INICIANDO PROCESO DE LOGIN ===")
            self.driver = self._configurar_driver()
            self.driver.get(self.url)
            logger.info(f"Navegando a: {self.url}")
            
            # Esperar a que cargue la página de login
            wait = WebDriverWait(self.driver, 15)
            
            # ============================================================
            # IMPORTANTE: AJUSTA ESTOS SELECTORES SEGÚN TU SISTEMA
            # ============================================================
            
            # Opción 1: Por ID (más confiable)
            try:
                logger.info("Buscando campos de login...")
                usuario_input = wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_input = self.driver.find_element(By.ID, "password")
                login_button = self.driver.find_element(By.ID, "login-btn")
                
            except:
                # Opción 2: Por NAME
                logger.info("Intento con selectores NAME...")
                usuario_input = wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_input = self.driver.find_element(By.NAME, "password")
                login_button = self.driver.find_element(By.NAME, "login")
            
            # Ingresar credenciales
            logger.info("Ingresando credenciales...")
            usuario_input.clear()
            usuario_input.send_keys(self.usuario)
            
            password_input.clear()
            password_input.send_keys(self.password)
            
            # Hacer clic en login
            logger.info("Haciendo clic en botón de login...")
            login_button.click()
            
            # Esperar a que cargue el dashboard (ajusta según tu sistema)
            time.sleep(3)
            
            # Verificar que el login fue exitoso
            # Ajusta esta verificación según tu sistema
            current_url = self.driver.current_url
            if "dashboard" in current_url.lower() or "home" in current_url.lower():
                logger.info("✅ Login exitoso")
                return True
            
            logger.info("✅ Login completado (verificar manualmente)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en login: {e}")
            if self.driver:
                # Tomar screenshot para debugging
                screenshot_path = os.path.join(self.download_dir, "error_login.png")
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot guardado en: {screenshot_path}")
                self.driver.quit()
            return False
    
    def obtener_precios(self, cadena):
        """
        Navega al sistema, selecciona la cadena y descarga el archivo
        
        Args:
            cadena: Nombre de la cadena
        
        Returns:
            str: Ruta del archivo descargado, None si hubo error
        """
        try:
            if not self.driver:
                logger.info("Driver no inicializado, realizando login...")
                if not self.login():
                    logger.error("No se pudo iniciar sesión")
                    return None
            
            wait = WebDriverWait(self.driver, 20)
            
            # ============================================================
            # PASO 1: NAVEGAR A LA SECCIÓN DE PRECIOS
            # ============================================================
            logger.info("=== NAVEGANDO A SECCIÓN DE PRECIOS ===")
            
            # AJUSTA ESTE SELECTOR SEGÚN TU SISTEMA
            # Ejemplo 1: Si es un link con texto
            try:
                menu_precios = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Precios"))
                )
                menu_precios.click()
                logger.info("✅ Click en menú Precios")
            except:
                # Ejemplo 2: Si es un link parcial
                try:
                    menu_precios = wait.until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Precio"))
                    )
                    menu_precios.click()
                    logger.info("✅ Click en menú Precios (partial)")
                except:
                    # Ejemplo 3: Si es por ID
                    menu_precios = wait.until(
                        EC.element_to_be_clickable((By.ID, "menu-precios"))
                    )
                    menu_precios.click()
                    logger.info("✅ Click en menú Precios (ID)")
            
            time.sleep(2)  # Esperar a que cargue el formulario
            
            # ============================================================
            # PASO 2: SELECCIONAR LA CADENA
            # ============================================================
            logger.info(f"=== SELECCIONANDO CADENA: {cadena} ===")
            
            # AJUSTA ESTE SELECTOR SEGÚN TU SISTEMA
            # Ejemplo 1: Si es un dropdown/select
            try:
                select_cadena = Select(wait.until(
                    EC.presence_of_element_located((By.ID, "select-cadena"))
                ))
                select_cadena.select_by_visible_text(cadena)
                logger.info(f"✅ Cadena seleccionada: {cadena}")
            except:
                # Ejemplo 2: Si es por NAME
                try:
                    select_cadena = Select(wait.until(
                        EC.presence_of_element_located((By.NAME, "cadena"))
                    ))
                    select_cadena.select_by_visible_text(cadena)
                    logger.info(f"✅ Cadena seleccionada (NAME): {cadena}")
                except Exception as e:
                    logger.warning(f"No se pudo seleccionar cadena: {e}")
            
            time.sleep(1)
            
            # ============================================================
            # PASO 3: SELECCIONAR "TODAS LAS SUCURSALES"
            # ============================================================
            logger.info("=== SELECCIONANDO TODAS LAS SUCURSALES ===")
            
            # AJUSTA SEGÚN TU SISTEMA
            try:
                # Opción 1: Si hay un checkbox "Todas"
                checkbox_todas = wait.until(
                    EC.element_to_be_clickable((By.ID, "check-todas-sucursales"))
                )
                if not checkbox_todas.is_selected():
                    checkbox_todas.click()
                    logger.info("✅ Checkbox 'Todas' marcado")
            except:
                # Opción 2: Si hay un select con opción "Todas"
                try:
                    select_sucursal = Select(wait.until(
                        EC.presence_of_element_located((By.ID, "select-sucursal"))
                    ))
                    select_sucursal.select_by_visible_text("Todas")
                    logger.info("✅ Seleccionado 'Todas las sucursales'")
                except Exception as e:
                    logger.warning(f"No se pudo seleccionar sucursales: {e}")
            
            time.sleep(1)
            
            # ============================================================
            # PASO 4: HACER CLIC EN EL BOTÓN DE GENERAR/DESCARGAR
            # ============================================================
            logger.info("=== GENERANDO ARCHIVO ===")
            
            # Obtener lista de archivos antes de descargar
            archivos_antes = set(os.listdir(self.download_dir))
            
            # AJUSTA ESTE SELECTOR SEGÚN TU SISTEMA
            try:
                # Opción 1: Por ID
                boton_descargar = wait.until(
                    EC.element_to_be_clickable((By.ID, "btn-generar-reporte"))
                )
                boton_descargar.click()
                logger.info("✅ Click en botón generar")
            except:
                # Opción 2: Por texto del botón
                try:
                    boton_descargar = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generar')]"))
                    )
                    boton_descargar.click()
                    logger.info("✅ Click en botón generar (XPATH)")
                except:
                    # Opción 3: Por clase CSS
                    boton_descargar = wait.until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "btn-descargar"))
                    )
                    boton_descargar.click()
                    logger.info("✅ Click en botón generar (CLASS)")
            
            # ============================================================
            # PASO 5: ESPERAR A QUE SE DESCARGUE EL ARCHIVO
            # ============================================================
            logger.info("=== ESPERANDO DESCARGA ===")
            archivo_descargado = self._esperar_descarga(archivos_antes, timeout=60)
            
            if archivo_descargado:
                logger.info(f"✅ Archivo descargado: {archivo_descargado}")
                return archivo_descargado
            else:
                logger.error("❌ Timeout esperando descarga del archivo")
                return None
            
        except Exception as e:
            logger.error(f"❌ Error al obtener precios: {e}")
            if self.driver:
                screenshot_path = os.path.join(self.download_dir, f"error_descarga_{cadena}.png")
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot guardado en: {screenshot_path}")
            return None
    
    def _esperar_descarga(self, archivos_previos, timeout=60):
        """
        Espera a que se complete la descarga del archivo
        
        Args:
            archivos_previos: Set de archivos existentes antes de la descarga
            timeout: Tiempo máximo de espera en segundos
        
        Returns:
            str: Ruta del archivo descargado, None si timeout
        """
        tiempo_inicio = time.time()
        
        logger.info(f"Esperando descarga (timeout: {timeout}s)...")
        
        while time.time() - tiempo_inicio < timeout:
            archivos_actuales = set(os.listdir(self.download_dir))
            nuevos_archivos = archivos_actuales - archivos_previos
            
            # Filtrar archivos temporales de Chrome (.crdownload, .tmp)
            archivos_completos = [
                f for f in nuevos_archivos 
                if not f.endswith(('.crdownload', '.tmp')) 
                and (f.endswith('.xls') or f.endswith('.xlsx'))
            ]
            
            if archivos_completos:
                archivo = archivos_completos[0]
                ruta_completa = os.path.join(self.download_dir, archivo)
                
                # Esperar a que el archivo termine de escribirse
                time.sleep(1)
                
                # Renombrar con timestamp para evitar conflictos
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_sin_ext, extension = os.path.splitext(archivo)
                nuevo_nombre = f"{nombre_sin_ext}_{timestamp}{extension}"
                nueva_ruta = os.path.join(self.download_dir, nuevo_nombre)
                
                try:
                    os.rename(ruta_completa, nueva_ruta)
                    logger.info(f"Archivo renombrado a: {nuevo_nombre}")
                    return nueva_ruta
                except Exception as e:
                    logger.error(f"Error al renombrar: {e}")
                    return ruta_completa
            
            time.sleep(1)  # Esperar 1 segundo antes de verificar nuevamente
        
        logger.warning(f"Timeout después de {timeout} segundos")
        return None
    
    def logout(self):
        """Cierra la sesión y el navegador"""
        try:
            if self.driver:
                logger.info("Cerrando sesión...")
                # Intentar hacer logout en el sistema (ajusta según tu sistema)
                try:
                    logout_button = self.driver.find_element(By.ID, "logout-button")
                    logout_button.click()
                    time.sleep(1)
                except:
                    pass
                
                self.driver.quit()
                logger.info("✅ Sesión cerrada exitosamente")
        except Exception as e:
            logger.error(f"Error al cerrar sesión: {e}")
    
    def __enter__(self):
        """Permite usar la clase con context manager"""
        self.login()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la sesión automáticamente"""
        self.logout()


# ============================================================
# CLASE SIMULADA PARA PRUEBAS (SIN SELENIUM)
# ============================================================
class SistemaPreciosSimulado:
    """
    Clase simulada para pruebas sin necesidad de conectar al sistema real
    Úsala mientras configuras los selectores correctos
    """
    
    def __init__(self):
        self.download_dir = Config.DOWNLOAD_DIR
        os.makedirs(self.download_dir, exist_ok=True)
    
    def obtener_precios(self, cadena):
        """Genera un archivo Excel de prueba"""
        try:
            import pandas as pd
            
            logger.info(f"[SIMULADO] Generando archivo para {cadena}")
            
            # Datos de ejemplo
            datos = {
                'Producto': [f'Producto {i}' for i in range(1, 21)],
                'Precio': [round(10 + i * 2.5, 2) for i in range(1, 21)],
                'Stock': [100 + i * 10 for i in range(1, 21)],
                'Categoría': ['Bebidas', 'Comida', 'Postres'] * 7,
                'Sucursal': ['General'] * 20
            }
            
            df = pd.DataFrame(datos)
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Precios_General_{cadena.replace(' ', '_')}_{timestamp}.xlsx"
            ruta_archivo = os.path.join(self.download_dir, nombre_archivo)
            
            # Guardar archivo
            with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Precios')
                
                # Ajustar ancho de columnas
                worksheet = writer.sheets['Precios']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"[SIMULADO] Archivo generado: {ruta_archivo}")
            return ruta_archivo
            
        except Exception as e:
            logger.error(f"[SIMULADO] Error: {e}")
            return None