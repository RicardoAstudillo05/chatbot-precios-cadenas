<<<<<<< HEAD
# Chatbot de Telegram - Sistema de Consulta de Precios

Bot automatizado para consulta y descarga de listas de precios de cadenas de restaurantes. Los usuarios pueden solicitar archivos Excel con precios generales (todas las sucursales) de manera rápida y automática a través de Telegram.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-20.7-blue.svg)](https://python-telegram-bot.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Tabla de Contenidos

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [Modo Prueba vs Modo Producción](#-modo-prueba-vs-modo-producción)
- [Personalización](#-personalización)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribución](#-contribución)

---

## Características

-  **Bot de Telegram interactivo** con menús de botones
-  **Generación automática** de archivos Excel (.xlsx)
-  **16 cadenas de restaurantes** configuradas
-  **Precios generales** (incluye todas las sucursales)
-  **Respuesta instantánea** a solicitudes
-  **Sistema de autenticación** automática
-  **Logging completo** de operaciones
-  **Navegación intuitiva** con opciones de volver/cancelar
-  **Selenium WebDriver** para automatización web
-  **Gestión automática** de archivos temporales

---

##  Estructura del Proyecto

```
chatbot-precios-cadenas/
│
├──  bot.py                      # Script principal del bot de Telegram
│   └── Maneja la interacción con usuarios, menús y envío de archivos
│
├──  sistema_precios.py          # Módulo de automatización web
│   ├── SistemaPrecios            → Conexión real con Selenium
│   └── SistemaPreciosSimulado    → Sistema de pruebas (sin VPN)
│
├──  config.py                   # Configuración centralizada
│   ├── Variables de entorno
│   ├── Lista de cadenas
│   └── Validaciones
│
├──  requirements.txt            # Dependencias del proyecto
│   └── Librerías Python necesarias
│
├──  .env                        # Variables de entorno (NO SUBIR A GIT)
│   ├── Token del bot
│   ├── Credenciales del sistema
│   └── Configuraciones
│
├──  descargas/                  # Archivos temporales (se crea automáticamente)
│   └── Archivos Excel generados
│
├──  venv/                       # Entorno virtual de Python
│   └── Dependencias aisladas
│
└──  README.md                   # Este archivo
```

---

##  Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Software Necesario

| Software | Versión Mínima | Enlace de Descarga |
|----------|----------------|-------------------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| Google Chrome | Última versión | [google.com/chrome](https://www.google.com/chrome/) |
| Git | 2.0+ | [git-scm.com](https://git-scm.com/downloads) |

### Credenciales Requeridas

- ✅ Token de Bot de Telegram (obtener de [@BotFather](https://t.me/botfather))
- ✅ Acceso al sistema de precios (usuario y contraseña)
- ✅ VPN configurada (para sistema real)

---

##  Instalación

### Paso 1: Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/RicardoAstudillo05/chatbot-precios-cadenas.git

# Entrar al directorio
cd chatbot-precios-cadenas
```

### Paso 2: Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Deberías ver la instalación de:
- `python-telegram-bot==20.7` - API de Telegram
- `pandas==2.1.4` - Manipulación de datos
- `openpyxl==3.1.2` - Escritura de archivos Excel
- `selenium==4.15.2` - Automatización web
- `webdriver-manager==4.0.1` - Gestión automática de ChromeDriver
- `python-dotenv==1.0.0` - Carga de variables de entorno

### Paso 4: Verificar Instalación

```bash
python -c "import telegram; print('✅ Telegram Bot API')"
python -c "import pandas; print('✅ Pandas')"
python -c "import selenium; print('✅ Selenium')"
```

---

##  Configuración

### 1. Crear Token del Bot

1. Abre Telegram y busca [@BotFather](https://t.me/botfather)
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `Sistema de Precios Bot`
   - Username: `precios_cadenas_bot` (debe terminar en `bot`)
4. Copia el token que te proporciona

### 2. Configurar Variables de Entorno

Edita el archivo `.env` en la raíz del proyecto:

```env
# ============================================
# CONFIGURACIÓN DEL BOT DE TELEGRAM
# ============================================
TELEGRAM_BOT_TOKEN=tu_token_aqui

# ============================================
# CONFIGURACIÓN DEL SISTEMA DE PRECIOS
# ============================================
# URL del sistema web de precios
SISTEMA_URL=https://sistema.tuempresa.com/login

# Credenciales de acceso
SISTEMA_USUARIO=tu_usuario
SISTEMA_PASSWORD=tu_password

# ============================================
# CONFIGURACIÓN ADICIONAL
# ============================================
# Directorio donde se guardarán los archivos temporales
DOWNLOAD_DIR=./descargas

# Usuarios autorizados (IDs de Telegram separados por comas)
# Ejemplo: USUARIOS_AUTORIZADOS=123456789,987654321
# Dejar vacío para permitir a todos los usuarios
USUARIOS_AUTORIZADOS=

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

### 3. Configurar Cadenas

Si necesitas agregar o modificar cadenas, edita `config.py`:

```python
CADENAS = [
    "AMERICAN DELI PATIOS",
    "EL ESPAÑOL",
    "JUAN VALDEZ",
    # ... agregar más cadenas aquí
]
```

---

##  Uso

### Iniciar el Bot

```bash
# Asegúrate de estar en el entorno virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Ejecutar el bot
python bot.py
```

**Salida esperada:**
```
==================================================
Iniciando Bot de Consulta de Precios...
==================================================
INFO - ✅ Bot iniciado correctamente
INFO - 📋 Cadenas disponibles: 16
INFO - 🔄 Modo: GENERAL (todas las sucursales)
INFO - ⌨️  Presiona Ctrl+C para detener el bot
==================================================
```

### Flujo de Usuario

1. **Iniciar conversación**
   - Buscar el bot en Telegram
   - Enviar `/start`

2. **Seleccionar cadena**
   - Elegir de la lista de 16 cadenas disponibles
   - Confirmar selección

3. **Generar archivo**
   - El bot genera el archivo Excel
   - Descarga automática del archivo
   - El archivo incluye precios de todas las sucursales

4. **Recibir archivo**
   - Archivo Excel listo para usar
   - Incluye: Producto, Precio, Stock, Categoría, Sucursal

### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el proceso de consulta de precios |
| `/ayuda` o `/help` | Muestra información de ayuda |
| `/stats` | Ver estadísticas (solo administradores) |

---

##  Modo Prueba vs Modo Producción

###  MODO PRUEBA (Sin VPN - Recomendado para testing)

Usa datos simulados sin conectar al sistema real.

**Configuración:**

En `bot.py`, línea ~53:

```python
# Importar sistema simulado
from sistema_precios import SistemaPreciosSimulado
sistema = SistemaPreciosSimulado()
```

**Ventajas:**
- ✅ No requiere VPN
- ✅ No requiere credenciales reales
- ✅ Respuesta instantánea
- ✅ Perfecto para pruebas de interfaz

**Ejecutar:**
```bash
python bot.py
```

---

###  MODO PRODUCCIÓN (Con Sistema Real)

Conecta al sistema real usando Selenium.

#### Paso 1: Conectar a la VPN

Asegúrate de estar conectado a la VPN de la empresa.

#### Paso 2: Configurar Credenciales

Edita `.env` con las credenciales reales:
```env
SISTEMA_URL=https://sistema-real.empresa.com/login
SISTEMA_USUARIO=usuario_real
SISTEMA_PASSWORD=password_real
```

#### Paso 3: Identificar Selectores del Sistema

Este es el paso **MÁS IMPORTANTE**. Debes identificar los selectores HTML de tu sistema:

1. **Abre el sistema en Chrome**
   ```
   https://sistema-real.empresa.com/login
   ```

2. **Abre DevTools (F12)**
   - Click derecho → "Inspeccionar"
   - O presiona `F12`

3. **Activar el selector**
   - Click en el icono de flecha (arriba izquierda)
   - O presiona `Ctrl + Shift + C`

4. **Identificar elementos:**

   **a) Campo de Usuario:**
   ```html
   <!-- Ejemplo de lo que verás en DevTools -->
   <input id="username" name="user" type="text" />
   
   <!-- Anota el ID o NAME -->
   ✅ ID: "username"
   ✅ NAME: "user"
   ```

   **b) Campo de Contraseña:**
   ```html
   <input id="password" name="pass" type="password" />
   
   ✅ ID: "password"
   ```

   **c) Botón de Login:**
   ```html
   <button id="login-btn" class="btn-primary">Iniciar Sesión</button>
   
   ✅ ID: "login-btn"
   ```

   **d) Menú de Precios:**
   ```html
   <a href="/precios">Precios</a>
   
   ✅ Texto del link: "Precios"
   ```

   **e) Selector de Cadena:**
   ```html
   <select id="select-cadena" name="cadena">
       <option>AMERICAN DELI PATIOS</option>
       ...
   </select>
   
   ✅ ID: "select-cadena"
   ```

   **f) Checkbox/Select de "Todas las Sucursales":**
   ```html
   <input type="checkbox" id="check-todas-sucursales" />
   
   ✅ ID: "check-todas-sucursales"
   ```

   **g) Botón de Generar:**
   ```html
   <button id="btn-generar-reporte">Generar Reporte</button>
   
   ✅ ID: "btn-generar-reporte"
   ```

#### Paso 4: Actualizar `sistema_precios.py`

Edita el archivo `sistema_precios.py` y actualiza los selectores:

```python
# LÍNEA ~62 - Login
usuario_input = wait.until(
    EC.presence_of_element_located((By.ID, "TU_ID_AQUI"))  # ← Cambiar
)
password_input = self.driver.find_element(By.ID, "TU_ID_AQUI")  # ← Cambiar
login_button = self.driver.find_element(By.ID, "TU_ID_AQUI")  # ← Cambiar

# LÍNEA ~125 - Menú Precios
menu_precios = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "TU_TEXTO_AQUI"))  # ← Cambiar
)

# LÍNEA ~155 - Selector de Cadena
select_cadena = Select(wait.until(
    EC.presence_of_element_located((By.ID, "TU_ID_AQUI"))  # ← Cambiar
))

# LÍNEA ~175 - Checkbox Todas
checkbox_todas = wait.until(
    EC.element_to_be_clickable((By.ID, "TU_ID_AQUI"))  # ← Cambiar
)

# LÍNEA ~200 - Botón Generar
boton_descargar = wait.until(
    EC.element_to_be_clickable((By.ID, "TU_ID_AQUI"))  # ← Cambiar
)
```

#### Paso 5: Activar Modo Producción

En `bot.py`, línea ~53:

```python
# Cambiar de sistema simulado a real
from sistema_precios import SistemaPrecios  # ← Cambiar esta línea
sistema = SistemaPrecios()  # ← Cambiar esta línea
```

#### Paso 6: Probar con Navegador Visible

Antes de ejecutar en modo headless, comenta esta línea en `sistema_precios.py` (línea ~45):

```python
# Comentar esta línea para ver qué hace el navegador
# chrome_options.add_argument("--headless")
```

Esto te permitirá ver el navegador y verificar que los selectores son correctos.

#### Paso 7: Ejecutar en Producción

```bash
python bot.py
```

**Verificar en los logs:**
```
INFO - === INICIANDO PROCESO DE LOGIN ===
INFO - Navegando a: https://sistema-real.empresa.com
INFO - Buscando campos de login...
INFO - ✅ Login exitoso
INFO - === NAVEGANDO A SECCIÓN DE PRECIOS ===
INFO - ✅ Click en menú Precios
INFO - === SELECCIONANDO CADENA: JUAN VALDEZ ===
INFO - ✅ Cadena seleccionada: JUAN VALDEZ
...
```

---

##  Personalización

### Agregar Nuevas Cadenas

Edita `config.py`:

```python
CADENAS = [
    "AMERICAN DELI PATIOS",
    "EL ESPAÑOL",
    # ... cadenas existentes ...
    "NUEVA CADENA 1",  # ← Agregar aquí
    "NUEVA CADENA 2",
]
```

### Cambiar Mensajes del Bot

Edita `bot.py`, funciones:
- `start()` - Mensaje de bienvenida
- `mostrar_menu_cadenas()` - Menú de selección
- `generar_y_enviar_archivo()` - Mensajes de generación

### Configurar Usuarios Autorizados

Obtén tu ID de Telegram usando [@userinfobot](https://t.me/userinfobot), luego edita `.env`:

```env
USUARIOS_AUTORIZADOS=123456789,987654321,555555555
```

---

##  Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'telegram'"

**Solución:**
```bash
pip install python-telegram-bot==20.7
```

### Problema: "Error: Invalid token"

**Solución:**
1. Verifica que el token en `.env` sea correcto
2. No debe tener espacios ni comillas adicionales
3. Formato: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### Problema: "ChromeDriver not found"

**Solución:**
```bash
pip install webdriver-manager
```
El driver se descarga automáticamente en el primer uso.

### Problema: El bot no responde a comandos

**Solución:**
1. Verifica que el bot esté corriendo (revisa la consola)
2. Intenta detener el bot (Ctrl+C) y reiniciarlo
3. Verifica tu conexión a internet
4. Busca el bot exactamente con el username que configuraste

### Problema: "Timeout esperando descarga"

**Solución:**
1. Verifica que estés conectado a la VPN
2. Aumenta el timeout en `sistema_precios.py` línea ~223:
   ```python
   archivo_descargado = self._esperar_descarga(archivos_antes, timeout=120)  # 2 minutos
   ```
3. Verifica los selectores con navegador visible

### Problema: Login falla en sistema real

**Solución:**
1. Descomenta `# chrome_options.add_argument("--headless")` para ver el navegador
2. Verifica que los selectores sean correctos
3. Toma screenshot del error (se guarda automáticamente en `descargas/`)
4. Revisa los logs para ver dónde falla exactamente

### Problema: No se genera el archivo Excel

**Solución:**
1. Verifica que pandas esté instalado: `pip install pandas openpyxl`
2. Verifica permisos en carpeta `descargas/`
3. Revisa los logs para ver el error específico

---

##  Logs y Debugging

### Ver Logs en Tiempo Real

Los logs se muestran en la consola. Para guardarlos en archivo, modifica `bot.py`:

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),  # Guardar en archivo
        logging.StreamHandler()  # Mostrar en consola
    ]
)
```

### Nivel de Logs

Edita `.env` para cambiar el nivel:
```env
LOG_LEVEL=DEBUG  # Más detalle
LOG_LEVEL=INFO   # Normal (recomendado)
LOG_LEVEL=WARNING  # Solo advertencias y errores
```

---

##  Seguridad

###  IMPORTANTE - Nunca Subir a Git:

- ❌ `.env` - Contiene credenciales
- ❌ `descargas/` - Puede contener información sensible
- ❌ `*.log` - Puede contener información de usuarios

### ✅ Archivo `.gitignore` (ya incluido):

```gitignore
# Archivos de entorno
.env
*.env

# Archivos temporales
descargas/
*.xls
*.xlsx

# Logs
*.log

# Python
__pycache__/
*.pyc
venv/
```

---

##  Contribución

### Para el Equipo de Trabajo

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/RicardoAstudillo05/chatbot-precios-cadenas.git
   ```

2. **Crear rama para pruebas**
   ```bash
   git checkout -b pruebas/mi-nombre
   ```

3. **Hacer cambios y probar**
   ```bash
   # Editar archivos necesarios
   python bot.py  # Probar
   ```

4. **Subir cambios**
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin pruebas/mi-nombre
   ```

5. **Crear Pull Request** en GitHub

### Reportar Problemas

Si encuentras un bug o tienes una sugerencia:

1. Ve a [Issues](https://github.com/RicardoAstudillo05/chatbot-precios-cadenas/issues)
2. Click en "New Issue"
3. Describe el problema con:
   - Pasos para reproducir
   - Error exacto (mensaje o screenshot)
   - Sistema operativo y versión de Python

---

##  Soporte

### Contacto

- **Desarrollador:** Ricardo Astudillo
- **Repositorio:** [github.com/RicardoAstudillo05/chatbot-precios-cadenas](https://github.com/RicardoAstudillo05/chatbot-precios-cadenas)
- **Issues:** [Reportar problema](https://github.com/RicardoAstudillo05/chatbot-precios-cadenas/issues)

### Recursos Útiles

- [Documentación python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Chrome DevTools Tutorial](https://developer.chrome.com/docs/devtools/)

---

##  Notas Finales

### Checklist para Producción

- [ ] Token del bot configurado en `.env`
- [ ] Credenciales del sistema configuradas
- [ ] VPN funcionando
- [ ] Selectores identificados y actualizados
- [ ] Probado en modo visible (sin headless)
- [ ] Probado con al menos 3 cadenas diferentes
- [ ] Usuarios autorizados configurados (opcional)
- [ ] Logs revisados sin errores

### Próximas Mejoras

- [ ] Implementar sistema de estadísticas
- [ ] Agregar base de datos para historial
- [ ] Notificaciones por email
- [ ] Dashboard web para administración
- [ ] Soporte para filtros adicionales
- [ ] Programación de envíos automáticos
- [ ] Caché de archivos recientes

---

##  Licencia

Este proyecto es de uso interno para la empresa. Todos los derechos reservados.

---

**Desarrollado con ❤️ para automatizar procesos y mejorar la eficiencia del equipo**

*Última actualización: Enero 2026*
=======
# chatbot-precios-cadenas
>>>>>>> 955ee5ddc6bc2185d4df5503f756b5789faf10f9
