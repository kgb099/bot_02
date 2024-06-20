import asyncio
import websockets
import json
import os
from datetime import datetime

# Constantes
TICKERS = ["btcusdt", "ethusdt", "zilusdt"]  # Ejemplo de tickers
WS_URI = "wss://stream.binance.com:9443/ws"  # URI para la conexión WebSocket con Binance
RECONNECT_DELAY = 10  # Tiempo de espera entre intentos de reconexión en segundos
MAX_RECONNECT_MINUTES = 5  # Máximo tiempo continuo de intentos de reconexión antes de una pausa

def get_directory_path(ticker):
    """Genera la ruta del directorio para almacenar los precios del ticker."""
    now = datetime.now()
    year_dir = f"{now.year}"
    month_dir = f"{now.month:02}-{now.year}"
    day_dir = f"{now.day:02}-{now.month:02}"
    base_path = os.path.join("Prices", f"{ticker.upper()}_precio")
    return os.path.join(base_path, year_dir, month_dir, day_dir)

def ensure_directory_exists(path):
    """Asegura que el directorio exista, si no, lo crea."""
    os.makedirs(path, exist_ok=True)

def get_filename():
    """Genera un nombre de archivo basado en la hora actual para almacenar los precios."""
    now = datetime.now()
    return f"{now.hour:02}-00.json"

def save_price_to_file(ticker, price):
    """
    Guarda los datos del precio en un archivo JSON, agregando cada nuevo precio en una nueva línea dentro de un array JSON.
    
    Args:
    ticker (str): Ticker del activo.
    price (float): Precio del activo.
    """
    directory_path = get_directory_path(ticker)
    ensure_directory_exists(directory_path)
    filename = get_filename()
    file_path = os.path.join(directory_path, filename)
    timestamp = datetime.now().strftime("%M:%S")
    new_data = {"price": f"{float(price):.5f}", "timestamp": timestamp}
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r+') as file:
                # Intentar leer el contenido existente
                data = file.read().strip()
                if data:
                    file.seek(0)
                    file.truncate()
                    # Eliminar la última línea que es un corchete de cierre ']'
                    data = data[:-1].rstrip(',')
                    # Si el archivo no estaba vacío, agregar una coma al final
                    if data:
                        data += ',\n'
                    # Añadir nuevo dato y cerrar el array
                    data += json.dumps(new_data, indent=2) + '\n]'
                else:
                    # Si el archivo está vacío, iniciar un nuevo array JSON
                    data = '[\n' + json.dumps(new_data, indent=2) + '\n]'
                file.write(data)
        else:
            # Si el archivo no existe, crear uno nuevo y escribir el primer elemento de la lista
            with open(file_path, 'w') as file:
                data = '[\n' + json.dumps(new_data, indent=2) + '\n]'
                file.write(data)
    except IOError as e:
        print(f"Error al abrir o escribir en el archivo: {e}")


async def ticker_handler(ticker):
    """Maneja los mensajes entrantes del WebSocket para un ticker específico."""
    attempt_start_time = datetime.now()
    while True:
        try:
            # Configuración personalizada para el timeout y el intervalo de pings
            async with websockets.connect(WS_URI, ping_timeout=60, ping_interval=10) as websocket:
                stream_name = f"{ticker}@trade"
                subscribe_message = json.dumps({
                    "method": "SUBSCRIBE",
                    "params": [stream_name],
                    "id": 1
                })
                await websocket.send(subscribe_message)

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    price = data.get('p')
                    if price is not None:
                        save_price_to_file(ticker, price)
                    else:
                        print(f"No se encontraron datos de precio en el mensaje para {ticker}.")
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
            print(f"La conexión se cerró con error: {e}")
            current_time = datetime.now()
            if (current_time - attempt_start_time).seconds < MAX_RECONNECT_MINUTES * 60:
                print("Intentando reconectar...")
                await asyncio.sleep(RECONNECT_DELAY)
            else:
                print("Los intentos de reconexión superaron el tiempo límite. Esperando 5 minutos antes de reintentar...")
                await asyncio.sleep(300)  # Espera 5 minutos
                attempt_start_time = datetime.now()  # Reinicia el temporizador después de la espera
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

async def main():
    """Función principal para manejar múltiples tickers simultáneamente."""
    await asyncio.gather(*(ticker_handler(ticker) for ticker in TICKERS))

asyncio.run(main())  # Descomenta esta línea para ejecutar el script
