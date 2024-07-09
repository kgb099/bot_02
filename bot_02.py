import asyncio
import websockets
import json
import os
from dotenv import load_dotenv, set_key
from binance import Client
from datetime import datetime,timedelta
from telegram import Bot
from telegram.error import RetryAfter

dotenv_path = '.env'
load_dotenv(dotenv_path, override=True)
#token de telegram
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PAR = "BTC"
ESTABLE = "USDT"
symbol = PAR+ESTABLE


#permite usar las apis lo de vuelve como tupla
def apis_key_y_secert():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    return(api_key,api_secret)


def modificar_apis_now():
    apis_key_viejas = apis_key_y_secert()[0]
    apis_secret_viejas = apis_key_y_secert()[1]
    fecha_de_expiracion = datetime.now() + timedelta(days=28)
    fecha_experacion = fecha_de_expiracion.strftime("%d-%m-%Y")

    while True:
        apis_key_now = input("cargar api key nueva: \n")
        apis_secret_now =input("cargar api secret nueva: \n")
        
        if apis_key_now != apis_key_viejas and apis_secret_now != apis_secret_viejas:
           set_key(dotenv_path, "API_KEY", apis_key_now) 
           set_key(dotenv_path, "API_SECRET", apis_secret_now)
           set_key(dotenv_path, "creacion", datetime.now().strftime("%d-%m-%Y"))
           set_key(dotenv_path, "experacion",fecha_experacion)
           print("Ambas claves han sido actualizadas con éxito.")
           break
        
        else:
          print("Ambas claves deben ser diferentes de las actuales. Por favor, ingrese nuevas claves.")


#revisa la expiracion de la clave
def verificacion_la_expiracion():
    experacion_str = os.getenv("experacion")
    if not experacion_str:
        return "No se encontró la variable de entorno 'experacion'", False
    
    else:
        experacion = datetime.strptime(experacion_str, '%d-%m-%Y')
        now = datetime.now()

        if experacion <= now:
            texto = "hay que cambiar las apis"
            resultado = False

        else:
            texto = "las apis estan correctas"
            resultado = True

        return texto, resultado


async def enviar_mensaje(texto):
    texto,resultado = verificacion_la_expiracion()
    if resultado == True:
        bot = Bot(token=TOKEN)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=texto)
        except RetryAfter as e:
            print(f"Excedido el control de inundación. Reintentar en {e.retry_after} segundos.")
            await asyncio.sleep(e.retry_after)
            await bot.send_message(chat_id=CHAT_ID, text=texto)
        finally:
            await bot.close()


def get_client():
    client = Client(apis_key_y_secert()[0],apis_key_y_secert()[1])  
    return client


#entrega todos el saldo de la cuenta o el saldo de un tiker espesifico
def clientes():
    client = get_client().get_account()
    clients = client['balances']
    balance1 = [client for client in clients if float(client['free']) > 0]
    activos = balance1
    for activo in activos:
        if activo['asset'] == ESTABLE:
            balance2 = f"Activo: {activo['asset']}, Saldo Disponible: {activo['free']}"
    balance3=balance1
    balance4=balance2
    return balance3, balance4


async def subscribe_to_price(symbol):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"

    async with websockets.connect(uri) as websocket:
        while True:
            try:

                message = await websocket.recv()
                data = json.loads(message)
                precio = data['c']
                
                print(f"Precio actual de {symbol}: {data['c']}")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    # Usar asyncio.run() para ejecutar la función asíncrona
    #asyncio.run(enviar_mensaje(verificacion_la_expiracion()[0]))
    mensaje, resultado = verificacion_la_expiracion()
    if not resultado:
        modificar_apis_now()
    else:
        mensaje
    print(clientes()[1])
    asyncio.run(subscribe_to_price(symbol=symbol))
    