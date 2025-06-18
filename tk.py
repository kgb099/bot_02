from binance.client import Client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

root = tk.Tk()
root.title("Trading Bot")
root.geometry("400x400")

# Configuración inicial
api_key = 'TU_API_KEY'
api_secret = 'TU_API_SECRET'
client = Client(api_key, api_secret)

symbol = 'BTCUSDT'
timeframe = '5m'  # Temporalidad de 5 minutos
capital = 1000  # Capital inicial en USDT
risk_per_trade = 0.02  # 2% de riesgo por operación
leverage = 10  # Apalancamiento 10x

# Configurar el apalancamiento
client.futures_change_leverage(symbol=symbol, leverage=leverage)

# Obtener datos históricos de futuros
def fetch_historical_data(symbol, timeframe, limit=500):
    klines = client.futures_klines(symbol=symbol, interval=timeframe, limit=limit)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close'] = data['close'].astype(float)
    return data

# Calcular RSI
def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Estrategia de trading
def trading_strategy(data):
    data['rsi'] = calculate_rsi(data)
    data['signal'] = 0
    data['signal'][data['rsi'] < 30] = 1  # Compra
    data['signal'][data['rsi'] > 70] = -1  # Venta
    return data

# Backtesting con apalancamiento
def backtest(data, initial_capital, risk_per_trade, leverage):
    current_capital = initial_capital  # Capital actualizado en cada operación
    position = 0
    trades = []
    
    for i in range(len(data)):
        if data['signal'].iloc[i] == 1 and position == 0:  # Compra
            # Calcular tamaño de posición con capital ACTUAL
            position_size = (current_capital * risk_per_trade * leverage) / data['close'].iloc[i]
            trades.append({
                'timestamp': data['timestamp'].iloc[i],
                'type': 'buy',
                'price': data['close'].iloc[i],
                'position': position_size,
                'capital_before': current_capital
            })
            position = position_size  # Abrir posición
            
        elif data['signal'].iloc[i] == -1 and position > 0:  # Venta
            # Calcular ganancia/pérdida
            pnl = position * (data['close'].iloc[i] - trades[-1]['price']) / trades[-1]['price']
            current_capital += pnl * leverage  # Actualizar capital
            
            trades.append({
                'timestamp': data['timestamp'].iloc[i],
                'type': 'sell',
                'price': data['close'].iloc[i],
                'position': position,
                'capital_after': current_capital
            })
            position = 0  # Cerrar posición
    
    return trades, current_capital

# Visualización de resultados
def plot_capital(trades):
    capitals = [trade['capital_before'] for trade in trades if 'capital_before' in trade]
    capitals.append(trades[-1]['capital_after']) if trades else None
    plt.figure(figsize=(14, 5))
    plt.plot([trade['timestamp'] for trade in trades if 'capital_before' in trade], capitals[:-1], label='Capital')
    plt.scatter(trades[-1]['timestamp'], capitals[-1], color='red', label='Capital Final')
    plt.title('Evolución del Capital')
    plt.legend()
    plt.show()

# Ejecución del código
data = fetch_historical_data(symbol, timeframe)
data = trading_strategy(data)
trades, final_capital = backtest(data, capital, risk_per_trade, leverage)
plot_capital(trades)

# Mostrar métricas
root.mainloop()
initial_capital = capital
final_capital = trades[-1]['position'] * trades[-1]['price'] / leverage if trades else capital
profit = final_capital - initial_capital
print(f"Capital inicial: {initial_capital} USDT")
print(f"Capital final: {final_capital} USDT")
print(f"Profit: {profit} USDT")