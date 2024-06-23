import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
from binance import Client
from datetime import datetime
from telegram import Bot
import asyncio

load_dotenv(override=True)

#permite usar las apis
def apis_key_y_secert():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    return(api_key,api_secret)

#revisa la expiracion de la clave
def verificacion_la_expiracion():
    experacion_str = os.getenv("experacion")
    experacion = datetime.strptime(experacion_str, '%d-%m-%Y')

    print(experacion)

    now = datetime.now()

    print(now)

    if experacion <= now:
        texto = "hay que cambiar las apis"

    else:
        texto = "las apis estan correctas"

    return texto

print(verificacion_la_expiracion())


# Token que te dio BotFather
TOKEN = os.getenv("BOT_TOKEN")
# ID del chat al que quieres enviar mensajes
CHAT_ID = os.getenv("CHAT_ID")
#texto que va dentro de el msj


async def enviar_mensaje(texto):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=texto)

if __name__ == "__main__":
    # Usar asyncio.run() para ejecutar la función asíncrona
    asyncio.run(enviar_mensaje(verificacion_la_expiracion()))



def get_client():
    client = Client(apis_key_y_secert()[0],apis_key_y_secert()[1])  
    return client

print(get_client())

def clientes():
    client = get_client().get_account()
    clients = client['balances']
    balance2 = [client for client in clients if float(client['free']) > 0]
    return balance2

activos = clientes()
for activo in activos:
    print(f"Activo: {activo['asset']}, Saldo Disponible: {activo['free']}")

def verificacion_de_apis():
    try:
        if():
            print("apis verificadas corectamente")
        raise
    except:
        print("tiempo caducado de las apis cambiarlas")
    
"""
PAR = "BTC"
ESTABLE = "USDT"
symbol = PAR+ESTABLE
print(symbol)

async def subscribe_to_price(symbol):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"

    async with websockets.connect(uri) as websocket:
        while True:
            try:

                message = await websocket.recv()
                data = json.loads(message)
                
                print(f"Precio actual de {symbol}: {data['c']}")
            except Exception as e:
                print(e)


# Ejemplo de suscripción al precio de BTCUSDT
asyncio.run(subscribe_to_price(symbol=symbol))"""