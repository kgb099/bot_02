import asyncio
import telegram_bot02 as tl
import time

def texto():
    return "hola mundo 5 minutos despues"

def cuenta_atras(segundos):
    for i in range(segundos, 0, -1):
        print(f"Esperando {i} segundos...", end='\r', flush=True)
        time.sleep(1)
    print("¡Tiempo terminado!           ")

cuenta_atras(40)

asyncio.run(tl.enviar_varios_mensajes([texto()]*1, espera=300))