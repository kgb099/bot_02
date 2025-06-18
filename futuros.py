import json
import os
import cliente_con_api # from cliente2 import client
import numpy as np
import indicadores.ind_rsi as ind_rsi
from telegram import Bot
from telegram.error import RetryAfter

client = cliente_con_api.client
calcular_rsi=ind_rsi.calcular_rsi

# Obtener todos los pares de futuros
futures_exchange_info = client.futures_exchange_info()
symbols = futures_exchange_info["symbols"]

# Extraer los pares de futuros
futures_pairs = [symbol["symbol"] for symbol in symbols]

resultados_rsi = {}

intervalos = ["5m", "15m", "1h", "4h"]

for symbol in futures_pairs:
    resultados_rsi[symbol] = {}
    for intervalo in intervalos:
        try:
            rsi = calcular_rsi(symbol, intervalo)
            if rsi is not None and not np.isnan(rsi):
                resultados_rsi[symbol][intervalo] = round(rsi, 2)
            else:
                resultados_rsi[symbol][intervalo] = None
        except Exception as e:
            print(f"Error con {symbol} [{intervalo}]: {e}")

# Guardar el diccionario de resultados en un archivo JSON
with open("futures_rsi.json", "w") as file:
    json.dump(resultados_rsi, file, indent=4)

# Filtrar los símbolos donde algún RSI de cualquier intervalo es >= 80
rsi_80_mas = {}
for symbol, intervalos in resultados_rsi.items():
    for intervalo, valor in intervalos.items():
        if valor is not None and valor >= 80:
            if symbol not in rsi_80_mas:
                rsi_80_mas[symbol] = {}
            rsi_80_mas[symbol][intervalo] = valor

print("Símbolos con RSI >= 80:")
for symbol, intervalos in rsi_80_mas.items():
    print(f"{symbol}: {intervalos}")

# Guardar el filtrado en otro archivo
with open("futures_rsi_80mas.json", "w") as file:
    json.dump(rsi_80_mas, file, indent=4)

# Filtrar los símbolos donde algún RSI de cualquier intervalo es <= 20
rsi_20_menos = {}
for symbol, intervalos in resultados_rsi.items():
    for intervalo, valor in intervalos.items():
        if valor is not None and valor <= 20:
            if symbol not in rsi_20_menos:
                rsi_20_menos[symbol] = {}
            rsi_20_menos[symbol][intervalo] = valor

print("Símbolos con RSI <= 20:")
for symbol, intervalos in rsi_20_menos.items():
    print(f"{symbol}: {intervalos}")

# Guardar el filtrado en otro archivo
with open("futures_rsi_20menos.json", "w") as file:
    json.dump(rsi_20_menos, file, indent=4)

print("Pares de futuros guardados en futures_pairs.json")
