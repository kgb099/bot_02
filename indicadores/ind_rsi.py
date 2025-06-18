from cliente_con_api import client_api
import pandas as pd

client=client_api()[0]
symbol = "ETHUSDT"  # Cambia esto al símbolo que desees analizar
# Importar las librerías necesarias
# Configuración del cliente de Binance
def calcular_rsi(symbol, interval='1m', limit=100, periodo=14):
    # Obtener velas (klines) del símbolo
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    cierres = [float(k[4]) for k in klines]  # k[4] es el precio de cierre

    # Calcular RSI
    df = pd.DataFrame(cierres, columns=['close'])
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]  # Último valor de RSI

print(calcular_rsi(symbol=symbol, interval="1m",limit= 100,periodo= 14))  # Ejemplo de uso