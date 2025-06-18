import os
import asyncio
from telegram import Bot
from telegram.error import RetryAfter

# Configuración del bot de Telegram
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def texto():
    return "Hola, soy un bot de Telegram. Estoy aquí para ayudarte con tus consultas sobre criptomonedas y trading."

bot = Bot(token=TOKEN)

async def enviar_mensaje(mensaje):
    
    try:
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    except RetryAfter as e:
        print(f"Excedido el control de inundación. Reintentar en {e.retry_after} segundos.")
        await asyncio.sleep(e.retry_after)
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    finally:
        await bot.close()

async def enviar_varios_mensajes(mensajes, espera=10):
    for mensaje in mensajes:
        await enviar_mensaje(mensaje)
        print(f"Mensaje enviado, esperando {espera} segundos...")
        await asyncio.sleep(espera)