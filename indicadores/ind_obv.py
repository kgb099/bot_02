from cliente_con_api import client_api
import pandas as pd

def calcular_obv_futuros(symbol="BTCUSDT", interval="1m", limit=100):
    """
    Calcula el indicador OBV (On Balance Volume) para datos de futuros de Binance.
    Retorna una serie de pandas con los valores de OBV.
    """
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    cierres = [float(k[4]) for k in klines]
    volumenes = [float(k[5]) for k in klines]

    df = pd.DataFrame({'close': cierres, 'volume': volumenes})
    obv = [0]
    for i in range(1, len(df)):
        if df['close'][i] > df['close'][i-1]:
            obv.append(obv[-1] + df['volume'][i])
        elif df['close'][i] < df['close'][i-1]:
            obv.append(obv[-1] - df['volume'][i])
        else:
            obv.append(obv[-1])
    df['obv'] = obv
    return df['obv']

# Ejemplo de uso:
obv = calcular_obv_futuros("BTCUSDT", "1m", 100)
print(obv.tail())