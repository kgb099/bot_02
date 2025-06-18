from cliente_con_api import client_api
import pandas as pd

def obtener_adx_futuros(symbol="BTCUSDT", interval="15m", limit=100):
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    high = [float(k[2]) for k in klines]
    low = [float(k[3]) for k in klines]
    close = [float(k[4]) for k in klines]
    df = pd.DataFrame({'high': high, 'low': low, 'close': close})

    period = 14
    df['tr'] = df[['high', 'low', 'close']].max(axis=1) - df[['high', 'low', 'close']].min(axis=1)
    df['plus_dm'] = df['high'].diff()
    df['minus_dm'] = df['low'].diff().abs()
    df['plus_dm'] = df['plus_dm'].where((df['plus_dm'] > df['minus_dm']) & (df['plus_dm'] > 0), 0.0)
    df['minus_dm'] = df['minus_dm'].where((df['minus_dm'] > df['plus_dm']) & (df['minus_dm'] > 0), 0.0)
    tr14 = df['tr'].rolling(window=period).sum()
    plus_dm14 = df['plus_dm'].rolling(window=period).sum()
    minus_dm14 = df['minus_dm'].rolling(window=period).sum()
    plus_di14 = 100 * (plus_dm14 / tr14)
    minus_di14 = 100 * (minus_dm14 / tr14)
    dx = 100 * (abs(plus_di14 - minus_di14) / (plus_di14 + minus_di14))
    adx = dx.rolling(window=period).mean()
    # Devuelve el último valor de cada uno
    return adx.iloc[-1], plus_di14.iloc[-1], minus_di14.iloc[-1]