import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# TOKEN de tu bot
TOKEN = "8541513790:AAFYFNeWnDWx8sWtMKZy_iw_F9Pj1zIZSXI"

# Listado de cadenas
CADENAS = [
    "AMERICAN DELI PATIOS", "EL ESPAÑOL", "JUAN VALDEZ",
    "BASKIN ROBBINS 1", "EMBUTSER", "KENTUCKY FRENCH CHICKEN",
    "CAFE ASTORIA", "FEDERER", "MENESTRAS DEL NEGRO", "CAJUN",
    "GUS", "CASA RES", "HELADERIAS KFC", "TROPI BURGUER",
    "EL CAPPO", "EL CAPPO II", "CINNABON", "DOLCE INCONTRO"
]


# Simulación del sistema de precios
# En producción, aquí integrarías tu clase SistemaPrecios
class SistemaPreciosSimulado:
    """Clase temporal para simular la generación de archivos"""
    
    def __init__(self):
        self.download_dir = "descargas"
        os.makedirs(self.download_dir, exist_ok=True)
    
    def obtener_precios(self, cadena):
        """
        Simula la descarga de un archivo XLS
        En producción, aquí llamarías al sistema real
        """
        try:
            logger.info(f"Generando archivo para {cadena} - GENERAL (todas las sucursales)")
            
            # Crear un archivo XLS simulado con pandas
            import pandas as pd
            
            # Datos de ejemplo
            datos = {
                'Producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
                'Precio': [10.50, 25.00, 15.75, 8.99, 12.50],
                'Stock': [100, 50, 75, 200, 150],
                'Categoría': ['Bebidas', 'Comida', 'Postres', 'Bebidas', 'Comida'],
                'Sucursal': ['Todas', 'Todas', 'Todas', 'Todas', 'Todas']
            }
            
            df = pd.DataFrame(datos)
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Precios_General_{cadena.replace(' ', '_')}_{timestamp}.xlsx"
            ruta_archivo = os.path.join(self.download_dir, nombre_archivo)
            
            # Guardar archivo con formato mejorado
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
            
            logger.info(f"Archivo generado: {ruta_archivo}")
            return ruta_archivo
            
        except Exception as e:
            logger.error(f"Error al generar archivo: {e}")
            return None


# Instancia del sistema
sistema = SistemaPreciosSimulado()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Función inicial /start"""
    user = update.effective_user
    logger.info(f"Usuario {user.first_name} ({user.id}) inició conversación")
    
    # Limpiar estado anterior
    context.user_data.clear()
    
    # Crear teclado inline
    keyboard = [
        [InlineKeyboardButton("✅ Continuar", callback_data="CONTINUAR")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="CANCELAR")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 ¡Hola, {user.first_name}!\n\n"
        "Bienvenido al *Sistema de Consulta de Precios* 📊\n\n"
        "Este bot te ayudará a obtener las listas de precios generales "
        "de nuestras cadenas de manera rápida y automática.\n\n"
        "Los archivos incluyen todas las sucursales.\n\n"
        "¿Deseas continuar?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todas las interacciones con botones"""
    query = update.callback_query
    user = query.from_user
    await query.answer()  # Importante: responde al callback
    
    logger.info(f"Usuario {user.first_name} presionó: {query.data}")
    
    # ==================== CANCELAR ====================
    if query.data == "CANCELAR":
        await query.edit_message_text(
            "❌ Proceso cancelado.\n\n"
            "Si deseas consultar precios nuevamente, usa el comando /start"
        )
        context.user_data.clear()
        return
    
    # ==================== CONTINUAR INICIAL ====================
    if query.data == "CONTINUAR" and not context.user_data.get("cadena"):
        await mostrar_menu_cadenas(query, context)
        return
    
    # ==================== SELECCIÓN DE CADENA ====================
    if query.data.startswith("CADENA_"):
        await seleccionar_cadena(query, context)
        return
    
    # ==================== VOLVER A CADENAS ====================
    if query.data == "VOLVER_CADENAS":
        context.user_data.pop("cadena", None)
        await mostrar_menu_cadenas(query, context)
        return
    
    # ==================== CONFIRMAR Y GENERAR ====================
    if query.data == "CONFIRMAR_GENERAR":
        await generar_y_enviar_archivo(query, context)
        return


async def mostrar_menu_cadenas(query, context):
    """Muestra el menú de cadenas disponibles"""
    # Crear botones en filas de 2 columnas para mejor visualización
    keyboard = []
    for i in range(0, len(CADENAS), 2):
        fila = []
        # Primera cadena de la fila
        fila.append(InlineKeyboardButton(
            f"{i+1}. {CADENAS[i][:20]}", 
            callback_data=f"CADENA_{i}"
        ))
        # Segunda cadena de la fila (si existe)
        if i + 1 < len(CADENAS):
            fila.append(InlineKeyboardButton(
                f"{i+2}. {CADENAS[i+1][:20]}", 
                callback_data=f"CADENA_{i+1}"
            ))
        keyboard.append(fila)
    
    # Botón de cancelar
    keyboard.append([InlineKeyboardButton("❌ Cancelar", callback_data="CANCELAR")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🏪 *Selecciona la cadena:*\n\n"
        "Por favor, elige la cadena para la cual necesitas la lista de precios.\n\n"
        "📌 _El archivo incluirá precios de todas las sucursales_",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def seleccionar_cadena(query, context):
    """Procesa la selección de una cadena y muestra confirmación"""
    index = int(query.data.split("_")[1])
    cadena_seleccionada = CADENAS[index]
    
    # Guardar en el contexto del usuario
    context.user_data["cadena"] = cadena_seleccionada
    context.user_data["cadena_index"] = index
    
    logger.info(f"Usuario {query.from_user.first_name} seleccionó: {cadena_seleccionada}")
    
    # Crear teclado de confirmación final
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar y Generar", callback_data="CONFIRMAR_GENERAR")],
        [InlineKeyboardButton("🔄 Cambiar Cadena", callback_data="VOLVER_CADENAS")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="CANCELAR")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📋 *Resumen de tu solicitud:*\n\n"
        f"🏪 Cadena: *{cadena_seleccionada}*\n"
        f"📍 Alcance: *Todas las sucursales*\n\n"
        f"¿Deseas generar el archivo de precios?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def generar_y_enviar_archivo(query, context):
    """Genera y envía el archivo de precios"""
    cadena = context.user_data.get("cadena")
    
    if not cadena:
        await query.edit_message_text(
            "❌ Error: No se ha seleccionado una cadena.\n\n"
            "Por favor, usa /start para comenzar nuevamente."
        )
        return
    
    # Mensaje de espera
    await query.edit_message_text(
        "⏳ *Generando archivo de precios...*\n\n"
        f"🏪 Cadena: {cadena}\n"
        f"📍 Alcance: Todas las sucursales\n\n"
        "Esto puede tomar unos momentos. Por favor, espera...",
        parse_mode='Markdown'
    )
    
    try:
        # Aquí se llamaría a tu sistema real
        # from sistema_precios import SistemaPrecios
        # sistema = SistemaPrecios(url, usuario, password)
        # ruta_archivo = sistema.obtener_precios(cadena)
        
        # Por ahora, usamos la simulación
        ruta_archivo = sistema.obtener_precios(cadena)
        
        if not ruta_archivo or not os.path.exists(ruta_archivo):
            raise Exception("No se pudo generar el archivo")
        
        # Obtener tamaño del archivo
        tamano = os.path.getsize(ruta_archivo)
        tamano_mb = tamano / (1024 * 1024)
        
        # Enviar el archivo
        with open(ruta_archivo, 'rb') as archivo:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=archivo,
                filename=os.path.basename(ruta_archivo),
                caption=(
                    f"✅ *Archivo generado exitosamente*\n\n"
                    f"🏪 Cadena: {cadena}\n"
                    f"📍 Alcance: Todas las sucursales\n"
                    f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                    f"📦 Tamaño: {tamano_mb:.2f} MB\n\n"
                    f"_Usa /start para generar otro archivo_"
                ),
                parse_mode='Markdown'
            )
        
        # Actualizar mensaje original
        await query.edit_message_text(
            f"✅ *Proceso completado exitosamente*\n\n"
            f"El archivo ha sido enviado. Revisa arriba 👆\n\n"
            f"Usa /start si necesitas generar otro archivo.",
            parse_mode='Markdown'
        )
        
        # Limpiar archivo temporal
        try:
            os.remove(ruta_archivo)
            logger.info(f"Archivo temporal eliminado: {ruta_archivo}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo temporal: {e}")
        
        logger.info(f"Archivo enviado exitosamente a {query.from_user.first_name} - Cadena: {cadena}")
        
        # Limpiar datos del usuario
        context.user_data.clear()
        
    except Exception as e:
        logger.error(f"Error al generar/enviar archivo: {e}")
        
        keyboard = [
            [InlineKeyboardButton("🔄 Reintentar", callback_data="CONFIRMAR_GENERAR")],
            [InlineKeyboardButton("🔄 Cambiar Cadena", callback_data="VOLVER_CADENAS")],
            [InlineKeyboardButton("❌ Cancelar", callback_data="CANCELAR")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ *Error al generar el archivo*\n\n"
            "Ocurrió un problema durante la generación del archivo. "
            "Esto puede deberse a:\n"
            "• Problemas de conexión con el sistema\n"
            "• Datos no disponibles temporalmente\n"
            "• Error en el servidor\n\n"
            "¿Deseas intentar nuevamente?",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de ayuda"""
    await update.message.reply_text(
        "🤖 *Sistema de Consulta de Precios*\n\n"
        "*Comandos disponibles:*\n"
        "/start - Iniciar solicitud de precios\n"
        "/ayuda - Mostrar esta ayuda\n\n"
        "*¿Cómo usar el bot?*\n"
        "1. Usa /start para comenzar\n"
        "2. Selecciona la cadena de tu interés\n"
        "3. Confirma y recibe tu archivo Excel\n\n"
        "*Características:*\n"
        "• Los archivos incluyen *todas las sucursales*\n"
        "• Formato Excel (.xlsx) listo para usar\n"
        "• Generación automática e instantánea\n"
        "• Datos actualizados del sistema\n\n"
        "💡 *Tip:* Puedes cancelar en cualquier momento\n\n"
        "_Si tienes problemas, contacta al administrador_",
        parse_mode='Markdown'
    )


async def estadisticas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para ver estadísticas (solo admin)"""
    user_id = update.effective_user.id
    
    # IDs de administradores (agregar los tuyos)
    ADMINS = []  # Ejemplo: [123456789, 987654321]
    
    if ADMINS and user_id not in ADMINS:
        await update.message.reply_text("❌ No tienes permisos para ver estadísticas.")
        return
    
    # Aquí podrías mostrar estadísticas reales
    await update.message.reply_text(
        "📊 *Estadísticas del Bot*\n\n"
        "Esta función estará disponible próximamente.\n\n"
        "Incluirá:\n"
        "• Total de solicitudes procesadas\n"
        "• Cadenas más consultadas\n"
        "• Archivos generados hoy\n"
        "• Usuarios activos\n"
        "• Horarios de mayor uso\n\n"
        "_Para activar esta función, implementa el sistema de registro_",
        parse_mode='Markdown'
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores globales del bot"""
    logger.error(f"Error en actualización: {context.error}")
    
    # Si hay un usuario activo, informarle del error
    if update and update.effective_user:
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text=(
                    "❌ *Error interno del bot*\n\n"
                    "Ha ocurrido un error inesperado. "
                    "Por favor, intenta nuevamente usando /start\n\n"
                    "Si el problema persiste, contacta al administrador."
                ),
                parse_mode='Markdown'
            )
        except:
            pass


def main():
    """Función principal"""
    logger.info("=" * 50)
    logger.info("Iniciando Bot de Consulta de Precios...")
    logger.info("=" * 50)
    
    try:
        # Crear aplicación
        application = Application.builder().token(TOKEN).build()
        
        # Agregar handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ayuda", ayuda))
        application.add_handler(CommandHandler("help", ayuda))
        application.add_handler(CommandHandler("stats", estadisticas))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Agregar manejador de errores
        application.add_error_handler(error_handler)
        
        # Iniciar bot
        logger.info("✅ Bot iniciado correctamente")
        logger.info(f"📋 Cadenas disponibles: {len(CADENAS)}")
        logger.info("🔄 Modo: GENERAL (todas las sucursales)")
        logger.info("⌨️  Presiona Ctrl+C para detener el bot")
        logger.info("=" * 50)
        
        # Ejecutar bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico al iniciar el bot: {e}")
    finally:
        logger.info("👋 Bot finalizado")


if __name__ == "__main__":
    main()