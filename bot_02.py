import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
from binance import Client
from datetime import datetime

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
        print("hay que cambiar las apis")
        return False
    else:
        print("toda via sirve")
        return True

print(verificacion_la_expiracion())

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

# def verificacion():
#      viejo = os.getenv("experacion")
#      viejo_datetime = datetime.strptime(viejo, "%d-%m-%Y")
     
#      print(viejo)
#      now = datetime.now()
#      if viejo_datetime >= now:# este if verifica la fecha
#          if Client(apis_key_y_secert()[0],apis_key_y_secert()[1]).get_account()['balances']:#este if verifica el cliente
#             return True
#          else:
#             return False

#      else:
#          return False

# if verificacion() == True:
#     print("Verdadero")
# else:
#     nueva_fecha_de_expiracion()
    

"""
def verificacion_de_apis():
    try:
        if():
            print("apis verificadas corectamente")
        raise
    except:
        print("tiempo caducado de las apis cambiarlas")
    except:
        print("problemas en las verificacion de las apis")
    

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