from cliente_con_api import client_api
import pandas as pd

def obtener_smas_futuros(symbol="ETHUSDT", interval="15m", limit=100):
    client = client_api()[0]
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    cierres = [float(k[4]) for k in klines]  # k[4] es el precio de cierre

    df = pd.DataFrame(cierres, columns=['close'])
    sma10 = df['close'].rolling(window=10).mean()
    sma55 = df['close'].rolling(window=55).mean()
    return sma10, sma55

def validar_cruce_medias(symbol="ETHUSDT", interval="15m", limit=100):
    sma10, sma55 = obtener_smas_futuros(symbol, interval, limit)
    # Tomamos los dos últimos valores para comparar el cruce
    if len(sma10) < 56 or len(sma55) < 56:
        return "No hay suficientes datos para validar el cruce."
    # Penúltima y última vela
    prev_sma10, prev_sma55 = sma10.iloc[-2], sma55.iloc[-2]
    last_sma10, last_sma55 = sma10.iloc[-1], sma55.iloc[-1]

    if prev_sma10 < prev_sma55 and last_sma10 > last_sma55:
        return "Cruce alcista: SMA10 cruza hacia arriba la SMA55."
    elif prev_sma10 > prev_sma55 and last_sma10 < last_sma55:
        return "Cruce bajista: SMA10 cruza hacia abajo la SMA55."
    else:
        return "No hay cruce de medias móviles en la última vela."

# Ejemplo de uso:
resultado = validar_cruce_medias("ETHUSDT", "15m", 100)
print(resultado)