from cliente_con_api import client_api
client = client_api()[0]

def obtener_precio_actual(client, symbol):
    """
    Devuelve el precio actual del símbolo en Binance Futuros.
    """
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

precio_actual = obtener_precio_actual(client, "ETHUSDT")
#print(f"Precio actual de ETHUSDT: {precio_actual}")