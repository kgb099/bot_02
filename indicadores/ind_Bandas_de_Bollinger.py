from cliente_con_api import client_api
import pandas as pd

def calcular_bollinger_futuros(symbol="BTCUSDT", interval="1m", limit=100, periodo=20, num_std=2):
    """
    Calcula las Bandas de Bollinger para datos de futuros de Binance.
    Retorna una tupla con (media, banda superior, banda inferior) como pandas.Series.
    """
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    cierres = [float(k[4]) for k in klines]  # Precio de cierre

    df = pd.DataFrame(cierres, columns=['close'])
    media = df['close'].rolling(window=periodo).mean()
    std = df['close'].rolling(window=periodo).std()
    banda_superior = media + num_std * std
    banda_inferior = media - num_std * std
    return media, banda_superior, banda_inferior

# Ejemplo de uso:
media, sup, inf = calcular_bollinger_futuros("BTCUSDT", "1m", 100, 20, 2)
print("Media:\n", media.tail())
print("Banda superior:\n", sup.tail())
print("Banda inferior:\n", inf.tail())