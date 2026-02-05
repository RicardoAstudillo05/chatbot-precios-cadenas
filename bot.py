import os
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from cadenas_config import CADENAS_LISTA, obtener_cdn_id, validar_cadena
from db_consultas import ConsultasDB
from credenciales_manager import obtener_credenciales_manager

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SELECCIONANDO_CADENA = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    logger.info(f"Usuario {user.id} ({user.username}) inicio el bot")
    
    mensaje_inicio = (
        f"Hola {user.first_name}\n\n"
        f"Bienvenido al Sistema Automático de Consulta de Precios\n\n"
        f"Puedo generar reportes de precios en formato Excel para cualquiera "
        f"de nuestras {len(CADENAS_LISTA)} cadenas.\n\n"
        f"El proceso incluye:\n"
        f"- Consulta automática de categorías\n"
        f"- Obtención de precios actualizados\n"
        f"- Generación de archivo Excel\n\n"
        f"Por favor, selecciona la cadena que deseas consultar:"
    )
    
    if update.callback_query:
        await update.callback_query.message.reply_text(mensaje_inicio)
    else:
        await update.message.reply_text(mensaje_inicio)
    
    return await mostrar_menu_cadenas(update, context)

async def mostrar_menu_cadenas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = []
    for i in range(0, len(CADENAS_LISTA), 2):
        fila = []
        cadena1 = CADENAS_LISTA[i]
        nombre_boton1 = cadena1 if len(cadena1) <= 25 else cadena1[:22] + "..."
        fila.append(
            InlineKeyboardButton(
                f"{i+1}. {nombre_boton1}",
                callback_data=f"cadena_{cadena1}"
            )
        )
        
        if i + 1 < len(CADENAS_LISTA):
            cadena2 = CADENAS_LISTA[i + 1]
            nombre_boton2 = cadena2 if len(cadena2) <= 25 else cadena2[:22] + "..."
            fila.append(
                InlineKeyboardButton(
                    f"{i+2}. {nombre_boton2}",
                    callback_data=f"cadena_{cadena2}"
                )
            )
        keyboard.append(fila)
    
    keyboard.append([InlineKeyboardButton("Cancelar", callback_data="cancelar")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensaje = (
        "SELECCIÓN DE CADENA\n\n"
        "Elige la cadena para la cual deseas generar el reporte de precios:\n\n"
        "El proceso puede tomar entre 30 segundos y 2 minutos"
    )
    
    # Verificar si el callback_query tiene un mensaje válido para editar
    if update.callback_query and update.callback_query.message:
        try:
            await update.callback_query.edit_message_text(
                mensaje,
                reply_markup=reply_markup
            )
        except Exception:
            # Si no se puede editar, enviar como mensaje nuevo
            await update.callback_query.message.reply_text(
                mensaje,
                reply_markup=reply_markup
            )
    else:
        await update.message.reply_text(
            mensaje,
            reply_markup=reply_markup
        )
    
    return SELECCIONANDO_CADENA

async def seleccionar_cadena(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer("Procesando solicitud...")
    
    cadena_seleccionada = query.data.replace("cadena_", "")
    
    if not validar_cadena(cadena_seleccionada):
        await query.edit_message_text(
            "ERROR\n\n"
            "Cadena no válida. Por favor, intenta de nuevo.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Volver al menú", callback_data="volver_menu")
            ]])
        )
        return SELECCIONANDO_CADENA
    
    cdn_id = obtener_cdn_id(cadena_seleccionada)
    logger.info(f"Usuario {update.effective_user.id} seleccionó: {cadena_seleccionada} (cdn_id: {cdn_id})")
    
    mensaje_inicial = (
        f"PROCESANDO SOLICITUD\n\n"
        f"Cadena: {cadena_seleccionada}\n"
        f"ID: {cdn_id}\n\n"
        f"Este proceso puede tomar entre 30 segundos y 2 minutos\n\n"
        f"Iniciando proceso..."
    )
    
    await query.edit_message_text(mensaje_inicial)
    
    archivo_generado = await generar_reporte(query, cadena_seleccionada)
    
    if archivo_generado:
        await enviar_archivo_excel(query, archivo_generado, cadena_seleccionada)
        return SELECCIONANDO_CADENA
    else:
        await query.message.reply_text(
            "ERROR AL GENERAR REPORTE\n\n"
            "No se pudo generar el reporte. Posibles causas:\n\n"
            "- Error de conexión a la base de datos\n"
            "- No hay datos disponibles para esta cadena\n"
            "- Problema al ejecutar las consultas\n"
            "- Timeout en la consulta\n\n"
            "Por favor, intenta nuevamente o selecciona otra cadena.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Reintentar", callback_data=f"cadena_{cadena_seleccionada}"),
                    InlineKeyboardButton("Menú", callback_data="volver_menu")
                ],
                [InlineKeyboardButton("Cancelar", callback_data="cancelar")]
            ])
        )
        return SELECCIONANDO_CADENA

async def generar_reporte(query, nombre_cadena: str) -> Optional[str]:
    try:
        await query.edit_message_text(
            f"PROCESANDO SOLICITUD\n\n"
            f"Cadena: {nombre_cadena}\n\n"
            f"Consultando categorías...\n"
            f"Obteniendo datos de precios...\n"
            f"Generando archivo Excel..."
        )
        
        consultas = ConsultasDB()
        if consultas.connection_string is None:
            logger.error("No se pudo obtener el connection string")
            return None
        
        if not consultas.conectar():
            logger.error("No se pudo conectar a la base de datos")
            return None
        
        cdn_id = obtener_cdn_id(nombre_cadena)
        
        categorias_df = consultas.obtener_categorias_por_cadena(cdn_id)
        if categorias_df is None or len(categorias_df) == 0:
            logger.error(f"No se encontraron categorías para {nombre_cadena}")
            consultas.desconectar()
            return None
        
        await query.edit_message_text(
            f"PROCESANDO SOLICITUD\n\n"
            f"Cadena: {nombre_cadena}\n\n"
            f"Categorías consultadas ({len(categorias_df)} encontradas)\n"
            f"Obteniendo datos de precios...\n"
            f"Generando archivo Excel..."
        )
        
        df_precios = consultas.ejecutar_stored_procedure_precios(cdn_id, categorias_df)
        if df_precios is None or df_precios.empty:
            logger.error(f"No se obtuvieron datos de precios para {nombre_cadena}")
            consultas.desconectar()
            return None
        
        await query.edit_message_text(
            f"PROCESANDO SOLICITUD\n\n"
            f"Cadena: {nombre_cadena}\n\n"
            f"Categorías consultadas ({len(categorias_df)} encontradas)\n"
            f"Datos de precios obtenidos ({len(df_precios)} registros)\n"
            f"Generando archivo Excel..."
        )
        
        archivo_generado = consultas.generar_archivo_excel(df_precios, categorias_df, nombre_cadena, cdn_id)
        consultas.desconectar()
        
        if archivo_generado:
            await query.edit_message_text(
                f"PROCESANDO SOLICITUD\n\n"
                f"Cadena: {nombre_cadena}\n\n"
                f"Categorías consultadas ({len(categorias_df)})\n"
                f"Datos de precios obtenidos ({len(df_precios)} registros)\n"
                f"Archivo Excel generado\n\n"
                f"Enviando archivo..."
            )
            return archivo_generado
            
    except Exception as e:
        logger.error(f"Error al generar reporte: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    return None

async def enviar_archivo_excel(query, ruta_archivo: str, nombre_cadena: str):
    try:
        tamano_archivo = os.path.getsize(ruta_archivo) / 1024
        nombre_archivo = os.path.basename(ruta_archivo)
        
        import pandas as pd
        try:
            df_full = pd.read_excel(ruta_archivo, sheet_name='Precios')
            total_filas = len(df_full)
            total_columnas = len(df_full.columns)
        except Exception as e:
            logger.warning(f"Error al leer archivo para info: {e}")
            total_columnas = "N/A"
            total_filas = "N/A"
        
        with open(ruta_archivo, 'rb') as archivo:
            await query.message.reply_document(
                document=archivo,
                filename=nombre_archivo,
                caption=(
                    f"REPORTE GENERADO EXITOSAMENTE\n\n"
                    f"Cadena: {nombre_cadena}\n"
                    f"Archivo: {nombre_archivo}\n"
                    f"Tamaño: {tamano_archivo:.2f} KB\n"
                    f"Registros: {total_filas} productos\n"
                    f"Columnas: {total_columnas}\n\n"
                    f"Características:\n"
                    f"- Filtros automáticos activados\n"
                    f"- Encabezados formateados\n"
                    f"- Columnas auto-ajustadas\n\n"
                    f"¿Deseas generar otro reporte?"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Nuevo reporte", callback_data="start_nuevo"),
                    InlineKeyboardButton("Finalizar", callback_data="finalizar_todo")
                ]])
            )
        
        logger.info(f"Archivo enviado exitosamente: {nombre_archivo}")
        
    except Exception as e:
        logger.error(f"Error al enviar archivo: {e}")
        await query.message.reply_text(
            "ERROR\n\n"
            "No se pudo enviar el archivo. Por favor, intenta nuevamente.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Volver al menú", callback_data="volver_menu")
            ]])
        )

async def start_nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer("Iniciando nuevo reporte...")
    
    chat_id = query.message.chat_id
    
    try:
        await query.message.delete()
    except Exception as e:
        logger.warning(f"No se pudo eliminar mensaje: {e}")
    
    user = update.effective_user
    
    mensaje_inicial = (
        f"Hola {user.first_name}\n\n"
        f"Bienvenido al Sistema Automático de Consulta de Precios\n\n"
        f"Puedo generar reportes de precios en formato Excel para cualquiera "
        f"de nuestras {len(CADENAS_LISTA)} cadenas.\n\n"
        f"El proceso incluye:\n"
        f"- Consulta automática de categorías\n"
        f"- Obtención de precios actualizados\n"
        f"- Generación de archivo Excel\n\n"
        f"Por favor, selecciona la cadena que deseas consultar:"
    )
    
    # Enviar mensaje de bienvenida
    await context.bot.send_message(
        chat_id=chat_id,
        text=mensaje_inicial
    )
    
    # Enviar menú de selección de cadenas
    return await enviar_menu_cadenas(context, chat_id)

async def enviar_menu_cadenas(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> int:
    """Envía el menú de selección de cadenas (sin depender de update)"""
    keyboard = []
    for i in range(0, len(CADENAS_LISTA), 2):
        fila = []
        cadena1 = CADENAS_LISTA[i]
        nombre_boton1 = cadena1 if len(cadena1) <= 25 else cadena1[:22] + "..."
        fila.append(
            InlineKeyboardButton(
                f"{i+1}. {nombre_boton1}",
                callback_data=f"cadena_{cadena1}"
            )
        )
        
        if i + 1 < len(CADENAS_LISTA):
            cadena2 = CADENAS_LISTA[i + 1]
            nombre_boton2 = cadena2 if len(cadena2) <= 25 else cadena2[:22] + "..."
            fila.append(
                InlineKeyboardButton(
                    f"{i+2}. {nombre_boton2}",
                    callback_data=f"cadena_{cadena2}"
                )
            )
        keyboard.append(fila)
    
    keyboard.append([InlineKeyboardButton("Cancelar", callback_data="cancelar")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensaje = (
        "SELECCIÓN DE CADENA\n\n"
        "Elige la cadena para la cual deseas generar el reporte de precios:\n\n"
        "El proceso puede tomar entre 30 segundos y 2 minutos"
    )
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=mensaje,
        reply_markup=reply_markup
    )
    
    return SELECCIONANDO_CADENA

async def finalizar_todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer("Sesión finalizada")
    
    await query.edit_message_text(
        "OPERACIÓN FINALIZADA\n\n"
        "Puedes iniciar nuevamente con /start en cualquier momento."
    )
    
    return ConversationHandler.END

async def volver_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer("Volviendo al menú...")
    
    return await mostrar_menu_cadenas(update, context)

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer("Operación cancelada")
    
    await query.edit_message_text(
        "OPERACIÓN CANCELADA\n\n"
        "Puedes iniciar nuevamente con /start en cualquier momento."
    )
    
    return ConversationHandler.END

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_ayuda = (
        "AYUDA - SISTEMA DE CONSULTA DE PRECIOS\n\n"
        "Comandos disponibles:\n"
        "/start - Iniciar el proceso de consulta\n"
        "/ayuda o /help - Mostrar esta ayuda\n\n"
        "¿Cómo funciona?\n"
        "1. Selecciona una cadena del menú\n"
        "2. El sistema consulta automáticamente:\n"
        "   - Categorías disponibles\n"
        "   - Precios actuales de todos los productos\n"
        "   - Información detallada por sucursal\n"
        "3. Recibes un archivo Excel listo para usar\n\n"
        f"Cadenas disponibles: {len(CADENAS_LISTA)}\n\n"
        "Tiempo de respuesta: 30-120 segundos\n\n"
        "Formato del archivo:\n"
        "- Archivo Excel (.xlsx)\n"
        "- Organizado por categorías\n"
        "- Incluye precios y disponibilidad\n\n"
        "¿Necesitas ayuda adicional?\n"
        "Contacta al administrador del sistema."
    )
    await update.message.reply_text(mensaje_ayuda)

def main():
    logger.info("Iniciando bot...")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN no encontrado en variables de entorno")
        logger.error("Verifica que el archivo .env exista y contenga el token")
        logger.error(f"Token esperado: 8541513790:AAFYFNeWnDWx8sWtMKZy_iw_F9Pj1zIZSXI")
        logger.error(f"Directorio actual: {os.getcwd()}")
        logger.error(f"Archivos en directorio: {os.listdir('.')}")
        
        # Intentar leer directamente el archivo .env
        try:
            with open('.env', 'r') as f:
                contenido = f.read()
                logger.info(f"Contenido de .env:\n{contenido}")
        except Exception as e:
            logger.error(f"No se pudo leer .env: {e}")
        
        return
    
    logger.info("Token encontrado en .env")
    
    logger.info("Verificando credenciales encriptadas...")
    
    cred_manager = obtener_credenciales_manager()
    if not cred_manager.cargar_credenciales():
        logger.error("No se pudieron cargar las credenciales encriptadas")
        logger.error("Verifica que existan los archivos secret.key y credenciales.enc")
        return
    
    if not cred_manager.validar_credenciales():
        logger.error("Las credenciales no son válidas")
        return
    
    logger.info("Credenciales validadas correctamente")
    logger.info("Verificando conexión a la base de datos...")
    
    consultas_test = ConsultasDB()
    if not consultas_test.conectar():
        logger.error("No se pudo conectar a la base de datos")
        return
    
    consultas_test.desconectar()
    logger.info("Conexión a BD verificada correctamente")
    
    application = Application.builder().token(token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECCIONANDO_CADENA: [
                CallbackQueryHandler(seleccionar_cadena, pattern='^cadena_'),
                CallbackQueryHandler(volver_menu, pattern='^volver_menu$'),
                CallbackQueryHandler(cancelar, pattern='^cancelar$'),
                CallbackQueryHandler(start_nuevo, pattern='^start_nuevo$'),
                CallbackQueryHandler(finalizar_todo, pattern='^finalizar_todo$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(start_nuevo, pattern='^start_nuevo$'),
            CallbackQueryHandler(finalizar_todo, pattern='^finalizar_todo$'),
        ],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('ayuda', ayuda))
    application.add_handler(CommandHandler('help', ayuda))
    
    logger.info("="*70)
    logger.info("BOT DE CONSULTA DE PRECIOS INICIADO")
    logger.info("="*70)
    logger.info(f"Cadenas configuradas: {len(CADENAS_LISTA)}")
    logger.info(f"Token de Telegram: {'*' * 20}{token[-8:]}")
    logger.info(f"Sistema de credenciales: Encriptado")
    logger.info(f"Conexión BD: Activa")
    logger.info("="*70)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()