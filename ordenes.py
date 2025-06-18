from binance.client import Client
from cliente_con_api import client_api
from precio import obtener_precio_actual
from typing import Optional, Dict
import asyncio
from telegram_bot02 import enviar_varios_mensajes

async def abrir_long(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01,
    leverage: int = 20
) -> Dict:
    """
    Ejecuta una operación de cobertura en el mercado de futuros de Binance.

    Parámetros:
    - client (object): Cliente de Binance (instancia del cliente de la API).
    - symbol (str): Par de trading (por ejemplo, 'ETHUSDT').
    - direccion (str): Dirección de la operación inicial ('long' o 'short').
    - apalancamiento (int): Nivel de apalancamiento (por ejemplo, 20).
    - porcentaje_riesgo (float): Porcentaje del saldo a usar en la operación inicial (por ejemplo, 0.01 = 1%).
    - porcentaje_cobertura (float): Porcentaje de distancia para colocar la cobertura (por ejemplo, 0.005 = 0.5%).

    Retorna:
    - dict: Resultado de la orden.
    """
    try:
        precio_entrada = obtener_precio_actual(client, symbol)
        hedge_distance = round(precio_entrada / (0.10 * leverage), 2)

        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        orden = client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=cantidad
        )

        mensaje = (
            f"[🟢 APERTURA LONG]\n"
            f"Symbol: {symbol}\n"
            f"Entry Price: {precio_entrada}\n"
            f"Quantity: {cantidad}\n"
            f"Leverage: {leverage}x\n"
            f"Hedge Distance: {hedge_distance}"
        )
        await enviar_varios_mensajes([mensaje])
        return orden

    except Exception as e:
        await enviar_varios_mensajes([
            f"[❌ ERROR AL ABRIR LONG]\n{e}"
        ])
        return {"error": str(e)}

async def abrir_short(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01,
    leverage: int = 20
) -> Dict:
    """
    Ejecuta una operación de cobertura en el mercado de futuros de Binance.

    Parámetros:
    - client (object): Cliente de Binance (instancia del cliente de la API).
    - symbol (str): Par de trading (por ejemplo, 'ETHUSDT').
    - direccion (str): Dirección de la operación inicial ('long' o 'short').
    - apalancamiento (int): Nivel de apalancamiento (por ejemplo, 20).
    - porcentaje_riesgo (float): Porcentaje del saldo a usar en la operación inicial (por ejemplo, 0.01 = 1%).
    - porcentaje_cobertura (float): Porcentaje de distancia para colocar la cobertura (por ejemplo, 0.005 = 0.5%).

    Retorna:
    - dict: Resultado de la orden.
    """
    try:
        precio_entrada = obtener_precio_actual(client, symbol)
        hedge_distance = round(precio_entrada / (0.10 * leverage), 2)

        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        orden = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=cantidad
        )

        mensaje = (
            f"[🔴 APERTURA SHORT]\n"
            f"Symbol: {symbol}\n"
            f"Entry Price: {precio_entrada}\n"
            f"Quantity: {cantidad}\n"
            f"Leverage: {leverage}x\n"
            f"Hedge Distance: {hedge_distance}"
        )
        await enviar_varios_mensajes([mensaje])
        return orden

    except Exception as e:
        await enviar_varios_mensajes([
            f"[❌ ERROR AL ABRIR SHORT]\n{e}"
        ])
        return {"error": str(e)}

async def cerrar_long(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01
) -> Dict:
    """
    Cierra una posición LONG (vendiendo) y notifica vía Telegram.
    """
    try:
        precio_actual = obtener_precio_actual(client, symbol)
        orden = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=cantidad
        )

        mensaje = (
            f"[🚪 CIERRE LONG]\n"
            f"Symbol: {symbol}\n"
            f"Exit Price: {precio_actual}\n"
            f"Quantity: {cantidad}"
        )
        await enviar_varios_mensajes([mensaje])
        return orden

    except Exception as e:
        await enviar_varios_mensajes([
            f"[❌ ERROR AL CERRAR LONG]\n{e}"
        ])
        return {"error": str(e)}

async def cerrar_short(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01
) -> Dict:
    """
    Cierra una posición SHORT (comprando) y notifica vía Telegram.
    """
    try:
        precio_actual = obtener_precio_actual(client, symbol)
        orden = client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=cantidad
        )

        mensaje = (
            f"[🚪 CIERRE SHORT]\n"
            f"Symbol: {symbol}\n"
            f"Exit Price: {precio_actual}\n"
            f"Quantity: {cantidad}"
        )
        await enviar_varios_mensajes([mensaje])
        return orden

    except Exception as e:
        await enviar_varios_mensajes([
            f"[❌ ERROR AL CERRAR SHORT]\n{e}"
        ])
        return {"error": str(e)}
