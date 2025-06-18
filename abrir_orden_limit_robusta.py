
from binance.client import Client
from cliente_con_api import client_api
from typing import Optional, Dict

def abrir_orden_limit(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01,
    precio_objetivo: Optional[float] = None,
    side: str = "BUY",
    leverage: int = 20
) -> Dict:
    """
    Coloca una orden LIMIT en Binance Futuros.

    Parámetros:
    - client (Client): Cliente autenticado de Binance.
    - symbol (str): Par de trading (ej. 'ETHUSDT').
    - cantidad (float): Cantidad del activo a operar.
    - precio_objetivo (float | None): Precio límite para la orden. Obligatorio.
    - side (str): 'BUY' para long o 'SELL' para short (por defecto 'BUY').
    - leverage (int): Nivel de apalancamiento (por defecto 20x).

    Retorna:
    - dict: Información de la orden creada o detalle del error.
    """
    if precio_objetivo is None:
        return {"error": "Debe especificar un precio objetivo para una orden LIMIT."}

    try:
        # Configurar el apalancamiento
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        # Crear la orden LIMIT
        orden = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            price=str(precio_objetivo),
            quantity=cantidad,
            timeInForce="GTC"
        )
        return orden

    except Exception as e:
        return {
            "error": "Error al crear orden LIMIT",
            "detalle": str(e),
            "parametros": {
                "symbol": symbol,
                "cantidad": cantidad,
                "precio_objetivo": precio_objetivo,
                "side": side,
                "leverage": leverage
            }
        }
