from cliente_con_api import client_api
import pandas as pd

def calcular_parabolic_sar_futuros(symbol="BTCUSDT", interval="1m", limit=100, af=0.02, af_max=0.2):
    """
    Calcula el indicador Parabolic SAR para datos de futuros de Binance.
    Retorna una serie de pandas con los valores de SAR.
    """
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    high = [float(k[2]) for k in klines]
    low = [float(k[3]) for k in klines]
    close = [float(k[4]) for k in klines]

    df = pd.DataFrame({'high': high, 'low': low, 'close': close})

    # Inicialización
    sar = [df['low'][0]]
    ep = df['high'][0]
    acc = af
    uptrend = True

    for i in range(1, len(df)):
        prev_sar = sar[-1]
        if uptrend:
            sar_new = prev_sar + acc * (ep - prev_sar)
            sar_new = min(sar_new, df['low'][i-1], df['low'][i])
            if df['low'][i] < sar_new:
                uptrend = False
                sar_new = ep
                ep = df['low'][i]
                acc = af
            else:
                if df['high'][i] > ep:
                    ep = df['high'][i]
                    acc = min(acc + af, af_max)
        else:
            sar_new = prev_sar + acc * (ep - prev_sar)
            sar_new = max(sar_new, df['high'][i-1], df['high'][i])
            if df['high'][i] > sar_new:
                uptrend = True
                sar_new = ep
                ep = df['high'][i]
                acc = af
            else:
                if df['low'][i] < ep:
                    ep = df['low'][i]
                    acc = min(acc + af, af_max)
        sar.append(sar_new)
    df['parabolic_sar'] = sar
    return df['parabolic_sar']

# Ejemplo de uso:
sar = calcular_parabolic_sar_futuros(symbol="BTCUSDT", interval="1m", limit=100)
print(sar.tail())