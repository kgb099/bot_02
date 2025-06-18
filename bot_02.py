import asyncio
import websockets
import json
import os, time
from dotenv import load_dotenv, set_key
from binance import Client
from datetime import datetime, timedelta
from telegram import Bot
from telegram.error import RetryAfter

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH, override=True)
# token de telegram
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PAR = "BTC"
ESTABLE = "USDT"
symbol = PAR + ESTABLE


def api_key_y_api_secret():
    """
    Obtiene la api key y api secret del archivo de configuracion de entorno (ej: .env).
    :return: api_key y api_secret -> tuple
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    return (api_key, api_secret)


def modificar_apis_now() -> tuple:
    """
    Compara fecha de expiracion de apis con la fecha actual si estan dentro del rango de 28 dias.
    - Si no cumple (vence) se solicita al usuario las nuevas api key y secret.\n
    Se comparan las nuevas apis con las recien vencidas.
    - Si no son iguales se guardan en el archivo de configuracion de entorno (ej: .env). \n
    :return: api_key_now, api_secret_now -> tuple
    """
    api_key_vieja = api_key_y_api_secret()[0]
    api_secret_vieja = api_key_y_api_secret()[1]
    fecha_de_expiracion = datetime.now() + timedelta(days=28)
    fecha_de_expiracion = fecha_de_expiracion.strftime("%d-%m-%Y")

    def cargar_nuevas_apis():
        return input("cargar api key nueva: \n"), input("cargar api secret nueva: \n")

    api_key_now, api_secret_now = cargar_nuevas_apis()
    if api_key_now == api_key_vieja or api_secret_now == api_secret_vieja:
        compare_apis = True
        while compare_apis:

            print(
                "Ambas claves deben ser diferentes de las actuales. \nPor favor, ingrese nuevas claves."
            )

            api_key_now, api_secret_now = cargar_nuevas_apis()
            compare_apis = api_key_now == api_key_vieja
            if not compare_apis:
                compare_apis = api_secret_now == api_secret_vieja

    # Si llega aca contamos con api key y api secret nuevas y distantas a las anteriores
    def save_api_key_y_api_secret(env_file=DOTENV_PATH):
        try:
            set_key(env_file, "API_KEY", api_key_now)
            set_key(env_file, "API_SECRET", api_secret_now)
            set_key(env_file, "creacion", datetime.now().strftime("%d-%m-%Y"))
            set_key(env_file, "experacion", fecha_de_expiracion)
            return (api_key_now, api_secret_now)
        except Exception as set_key_exception:
            return set_key_exception

    save_apis = save_api_key_y_api_secret(DOTENV_PATH)
    while type(save_apis) is Exception:
        print("Error saving api key y api_secret: ", save_apis)
        file_not_found_error = ""
        # resuelve error de archivo de configuracion
        if str(save_apis).__contains__(file_not_found_error):
            save_apis = save_api_key_y_api_secret(
                input("por favor indica el archivo de configuracion (ej: .env) \n-> ")
            )
            continue
        # reintento
        time.sleep(5)
        save_apis = save_api_key_y_api_secret(DOTENV_PATH)

    print("Ambas claves han sido actualizadas con éxito.")
    return save_apis


def verificacion_la_expiracion():
    """
    Obtiene la fecha de expiracion de la clave del archivo de configuracion de entorno (ej: .env).
    - Si no se encuentra se indica el mensaje. \n
    Se compara la fecha de expiracion de la clave con la fecha actual.
    - Si supera o no (vence) se indica el mensaje respectivo. \n
    :return: (texto, resultado) -> tuple
    """
    expiracion_str = os.getenv("expiracion")
    if not expiracion_str:
        return "No se encontró la variable de entorno 'expiracion'", False

    expiracion = datetime.strptime(expiracion_str, "%d-%m-%Y")
    now = datetime.now()

    if expiracion <= now:
        return "hay que cambiar las apis", False

    return "las apis estan correctas", True


async def enviar_mensaje(texto):
    """
    Obtiene resultado de la verificacion de la fecha de expiracion
    - Si cumple carga el bot y espera el envio de mensaje al chat indicado.
    - Para la excepción RetryAfter muestra mensaje, espera a resolver y reintenta envio.
    - cierra el bot al finalizar el proceso. \n
    :param texto: mensaje a mostrar
    """
    mensaje, resultado = verificacion_la_expiracion()
    if texto is None or len(texto) <= 0:
        texto = mensaje
    if resultado == True:
        bot = Bot(token=TOKEN)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=texto)
        except RetryAfter as e:
            print(
                f"Excedido el control de inundación. Reintentar en {e.retry_after} segundos."
            )
            await asyncio.sleep(e.retry_after)
            await bot.send_message(chat_id=CHAT_ID, text=texto)
        finally:
            await bot.close()


def get_client():
    """
    Obtiene el cliente de api usando el api_key_y_api_secret indicado. \n
    :return: instancia de Cliente Binance API
    """
    return Client(*api_key_y_api_secret())


def clientes():
    """
    Entrega todos el saldo de la cuenta o el saldo de un ticker especifico. \n
    :return: balances de la cuenta -> tuple
    """
    client = get_client().get_account()
    clients = client["balances"]
    balance1 = [client for client in clients if float(client["free"]) > 0]
    activos = balance1
    for activo in activos:
        asset_activo = activo["asset"]
        if asset_activo == ESTABLE:
            balance2 = f"Activo: {asset_activo}, Saldo Disponible: {activo['free']}"
    balance3 = balance1
    balance4 = balance2
    return balance3, balance4


def get_directory_path(symbol):
    """
    Genera la ruta del directorio para almacenar los precios del ticker. \n
    :param symbol: ticker indicado -> string
    :return: ruta de directorio en formato: Prices/ {ticker}_precio / {fecha} / .
    """
    now = datetime.now()
    year_dir = f"{now.year}"
    month_dir = f"{now.month:02}-{now.year}"
    day_dir = f"{now.day:02}-{now.month:02}"
    base_path = os.path.join("Prices", f"{symbol.upper()}_precio")
    return os.path.join(base_path, year_dir, month_dir, day_dir)


def ensure_directory_exists(path):
    """
    Asegura que el directorio exista, si no, lo crea. \n
    :param path: ruta indicada
    """
    os.makedirs(path, exist_ok=True)


def get_filename():
    """
    Genera un nombre de archivo para almacenar los precios. \n
    :return: nombre de archivo basado en la hora actual
    """
    now = datetime.now()
    return f"{now.hour:02}-00.json"


def save_price_to_file(symbol, price):
    """
    Guarda los datos del precio en un archivo JSON, agregando cada nuevo precio en una nueva línea
    dentro de un array JSON. \n
    :param ticker: Ticker del activo.
    :param price: Precio del activo.
    """
    directory_path = get_directory_path(symbol)
    ensure_directory_exists(directory_path)
    filename = get_filename()
    file_path = os.path.join(directory_path, filename)
    timestamp = datetime.now().strftime("%M:%S")
    new_data = {"price": f"{float(price):.5f}", "timestamp": timestamp}

    try:
        if os.path.exists(file_path):
            with open(file_path, "r+") as file:
                # Intentar leer el contenido existente
                data = file.read().strip()
                if data:
                    file.seek(0)
                    file.truncate()
                    # Eliminar la última línea que es un corchete de cierre ']'
                    data = data[:-1].rstrip(",")
                    # Si el archivo no estaba vacío, agregar una coma al final
                    if data:
                        data += ",\n"
                    # Añadir nuevo dato y cerrar el array
                    data += json.dumps(new_data, indent=2) + "\n]"
                else:
                    # Si el archivo está vacío, iniciar un nuevo array JSON
                    data = "[\n" + json.dumps(new_data, indent=2) + "\n]"
                file.write(data)
        else:
            # Si el archivo no existe, crear uno nuevo y escribir el primer elemento de la lista
            with open(file_path, "w") as file:
                data = "[\n" + json.dumps(new_data, indent=2) + "\n]"
                file.write(data)
    except IOError as e:
        print(f"Error al abrir o escribir en el archivo: {e}")


async def subscribe_to_price(symbol, queue):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"

    async with websockets.connect(uri) as websocket:
        recibir_precio_socket(queue, websocket)


async def recibir_precio_socket(queue, websocket):
    try:
        message = await websocket.recv()
        data = json.loads(message)
        precio = data["c"]

        print(f"Precio actual de {symbol}: {precio}")

        # Poner el precio en la cola
        await queue.put(precio)

    except Exception as e:
        print(e)

    recibir_precio_socket(queue, websocket)


async def procesar_precios(queue, get_directory_path):
    try:
        precio = await queue.get()
    except Exception as precio_E:
        precio = None

    if precio is not None:
        # Guardar el precio en un archivo JSON (opcional)
        with open("precios.json", "a") as f:
            json.dump(
                {"timestamp": datetime.datetime.now().isoformat(), "precio": precio}, f
            )
            f.write("\n")

        # Procesar el precio (reemplaza esta línea con tu lógica)
        print(f"Procesando el precio: {precio}")

    # Simulación de una operación asíncrona (opcional)
    await asyncio.sleep(1)
    await procesar_precios(queue, get_directory_path)


async def verificar_apis_periodicamente():
    while True:
        # Verificar las APIs cada 28 días
        await asyncio.sleep(5)  # 28 días en segundos
        mensaje, resultado = verificacion_la_expiracion()
        if not resultado:
            modificar_apis_now()
        else:
            await enviar_mensaje(mensaje)


async def main(symbol):
    queue = asyncio.Queue()

    # Crear tareas para obtener y procesar precios
    obtener_precio_task = asyncio.create_task(subscribe_to_price(symbol, queue))
    procesar_precio_task = asyncio.create_task(procesar_precios(queue))
    verificar_apis_task = asyncio.create_task(verificar_apis_periodicamente())

    # Ejecutar todas las tareas
    await asyncio.gather(obtener_precio_task, procesar_precio_task, verificar_apis_task)


if __name__ == "__main__":
    mensaje, resultado = verificacion_la_expiracion()

    if not resultado:
        modificar_apis_now()
    else:
        asyncio.run(enviar_mensaje(mensaje))

    print(clientes()[1])
    symbol = "btcusdt"
    asyncio.run(main(symbol))


def get_directory_path(symbol):
    """Genera la ruta del directorio para almacenar los precios del ticker."""
    now = datetime.now()
    year_dir = f"{now.year}"
    month_dir = f"{now.month:02}-{now.year}"
    day_dir = f"{now.day:02}-{now.month:02}"
    base_path = os.path.join("Prices", f"{symbol.upper()}_precio")
    return os.path.join(base_path, year_dir, month_dir, day_dir)
