from cliente_con_api import client_api
import numpy as np

symbols = "ETHUSDT"  # Cambia esto al símbolo que desees analizar

def obtener_vwap_futuros(symbol=symbols, interval="1m", limit=100):
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    # Extraer precios y volúmenes
    high = np.array([float(k[2]) for k in klines])
    low = np.array([float(k[3]) for k in klines])
    close = np.array([float(k[4]) for k in klines])
    volume = np.array([float(k[5]) for k in klines])

    typical_price = (high + low + close) / 3
    vwap = np.sum(typical_price * volume) / np.sum(volume)
    return vwap

# Ejemplo de uso:
vwap = obtener_vwap_futuros(symbols, "1m", 100)
print(f"VWAP: {vwap}")