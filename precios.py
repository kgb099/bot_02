import os
import json
import time
from datetime import datetime, timedelta
from cliente_con_api import client_api

Client = client_api()[0]
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
VELAS_POR_PEDIDO = 720  # 12 horas * 60 minutos

def save_klines_by_hour(symbol, klines, base_dir="F:/precios"):
    grouped = {}
    for kline in klines:
        dt = datetime.fromtimestamp(kline[0] / 1000)
        key = (dt.year, dt.month, dt.day, dt.hour)
        grouped.setdefault(key, []).append(kline)

    for (year, month, day, hour), kline_list in grouped.items():
        dir_path = os.path.join(base_dir, symbol, f"{year}-{month:02}", f"{day:02}")
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{hour:02}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            data.extend(kline_list)
        else:
            data = kline_list
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

def get_first_kline_time(symbol, interval):
    klines = Client.get_historical_klines(symbol, interval, "1 Jan, 2017", limit=1)
    if klines:
        return klines[0][0]
    return None

def fetch_all_klines(symbol, interval):
    end_time = int(time.time() * 1000)
    first_time = get_first_kline_time(symbol, interval)
    if not first_time:
        print("No se encontraron datos.")
        return

    while end_time > first_time:
        # Calcula el start_time para pedir exactamente 10 horas hacia atrás
        start_time = end_time - (VELAS_POR_PEDIDO * 60 * 1000)
        if start_time < first_time:
            start_time = first_time

        klines = Client.get_klines(symbol=symbol, interval=interval, startTime=start_time, endTime=end_time, limit=VELAS_POR_PEDIDO)
        if not klines:
            break
        save_klines_by_hour(symbol, klines)
        # Retrocede: el próximo end_time será el open_time del primer kline menos 1 ms
        end_time = klines[0][0] - 1
        print(f"Descargadas hasta: {datetime.fromtimestamp(end_time/1000)}")
        time.sleep(0.5)  # Para evitar rate limits

if __name__ == "__main__":
    fetch_all_klines(SYMBOL, INTERVAL)