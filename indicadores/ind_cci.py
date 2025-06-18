from cliente_con_api import client_api
import pandas as pd

def calcular_cci_futuros(symbol="BTCUSDT", interval="1m", limit=100, periodo=20):
    """
    Calcula el CCI (Commodity Channel Index) para datos de futuros de Binance.
    """
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    high = [float(k[2]) for k in klines]
    low = [float(k[3]) for k in klines]
    close = [float(k[4]) for k in klines]

    df = pd.DataFrame({'high': high, 'low': low, 'close': close})
    tp = (df['high'] + df['low'] + df['close']) / 3  # Precio típico
    ma = tp.rolling(window=periodo).mean()
    md = tp.rolling(window=periodo).apply(lambda x: (abs(x - x.mean())).mean())
    cci = (tp - ma) / (0.015 * md)
    return cci

# Ejemplo de uso:
cci = calcular_cci_futuros("BTCUSDT", "1m", 100, 20)
print(cci.tail())