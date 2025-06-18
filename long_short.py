from binance.client import Client
from cliente_con_api import client_api
from saldo import obtener_saldo_usdt
from precio import obtener_precio_actual
from typing import Optional, Dict

def abrir_long(
    client: Client = client_api()[0],
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01,
    precio: Optional[float] = None,
    leverage: int = 20
) -> Dict:
    """
    Abre una posición LONG en Binance Futuros.

    Parámetros:
    - client (client_api): Cliente de Binance propio.
    - symbol (str): Par de trading (ej. 'ETHUSDT').
    - cantidad (float): Cantidad del activo a comprar.
    - precio (float | None): No se usa en esta función (placeholder opcional).
    - leverage (int): Nivel de apalancamiento (por defecto 20x).

    Retorna:
    - dict: Información de la orden creada.
    """
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    orden = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='MARKET',
        quantity=cantidad
    )
    return orden

def abrir_short(
    client: Client = client_api()[0],  # Aquí ejecutás la función y usás el tipo correcto
    symbol: str = "ETHUSDT",
    cantidad: float = 0.01,
    precio: Optional[float] = None,
    leverage: int = 20
) -> Dict:
    """
    Abre una posición SHORT en Binance Futuros.

    Parámetros:
    - client (Client): Cliente autenticado de Binance.
    - symbol (str): Par de trading (ej. 'ETHUSDT').
    - cantidad (float): Cantidad del activo a vender.
    - precio (float | None): Placeholder opcional, no usado en esta función.
    - leverage (int): Nivel de apalancamiento (por defecto 20x).

    Retorna:
    - dict: Información de la orden creada.
    """
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    orden = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='MARKET',
        quantity=cantidad
    )
    return orden


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

def operar_con_cobertura(
    apalancamiento: int = 20,
    client: object = client_api,
    symbol: str = "ETHUSDT",
    direccion: str = "long",
    porcentaje_riesgo: float = 0.01,
    porcentaje_cobertura: float = 0.01
) -> None:
    """
    Ejecuta una operación de cobertura en el mercado de futuros de Binance.

    Parámetros:
    - client (object): Cliente de Binance (instancia del cliente de la API).
    - symbol (str): Par de trading (ejemplo: 'ETHUSDT').
    - direccion (str): Dirección de la operación principal ('long' o 'short').
    - apalancamiento (int): Nivel de apalancamiento (ejemplo: 20).
    - porcentaje_riesgo (float): Porcentaje del saldo total a usar en la operación inicial (ej: 0.01 = 1%).
    - porcentaje_cobertura (float): Porcentaje de distancia para colocar la cobertura (ej: 0.01 = 1%).

    Retorna:
    - None
    """

    precio_actual = obtener_precio_actual(client, symbol=symbol)
    saldo_usdt = obtener_saldo_usdt(client)
    cantidad = round((saldo_usdt * porcentaje_riesgo * apalancamiento) / precio_actual, 4)

    # Determinar dirección opuesta para cobertura
    tipo_cobertura = "short" if direccion == "long" else "long"

    # Calcular precio objetivo de cobertura según riesgo y apalancamiento
    resultado_cobertura = calcular_cobertura(
        precio_entrada=precio_actual,
        apalancamiento=apalancamiento,
        riesgo_pct=porcentaje_riesgo,
        tipo=tipo_cobertura
    )

    precio_cobertura = resultado_cobertura["precio_objetivo"]
    distancia_pct = resultado_cobertura["distancia_porcentual"]

    print(f"{direccion.capitalize()} abierto y cobertura {tipo_cobertura} limit en {precio_cobertura} "
          f"({distancia_pct}%) | Cantidad: {cantidad} | Precio entrada: {precio_actual}")

    # Ejecutar órdenes reales (comentadas por ahora)
    # if direccion == "long":
    #     abrir_long(client, symbol, cantidad)
    #     abrir_orden_limit(client, symbol, cantidad, precio_cobertura, side="SELL", leverage=apalancamiento)
    # elif direccion == "short":
    #     abrir_short(client, symbol, cantidad)
    #     abrir_orden_limit(client, symbol, cantidad, precio_cobertura, side="BUY", leverage=apalancamiento)

def calcular_cobertura(precio_entrada: float, apalancamiento: float, riesgo_pct: float = 0.10, tipo: str = "short") -> dict:
    """
    Calcula la distancia nominal de cobertura y el precio objetivo, según el apalancamiento y el porcentaje de riesgo.

    :param precio_entrada: Precio de entrada de la operación.
    :param apalancamiento: Nivel de apalancamiento (por ejemplo, 20 para 20x).
    :param riesgo_pct: Porcentaje de riesgo deseado (por defecto 10%).
    :param tipo: Tipo de operación ('long' o 'short') para calcular el precio objetivo.
    :return: Diccionario con la distancia en % y el precio objetivo.
    """
    distancia_pct = riesgo_pct / apalancamiento
    distancia_precio = round(precio_entrada * distancia_pct, 2)

    if tipo == "long":
        precio_objetivo = round(precio_entrada - distancia_precio, 2)
    elif tipo == "short":
        precio_objetivo = round(precio_entrada + distancia_precio, 2)
    else:
        raise ValueError("El tipo debe ser 'long' o 'short'.")

    return {
        "distancia_porcentual": round(distancia_pct * 100, 2),  # en %
        "precio_objetivo": precio_objetivo
    }

# Ejemplo de uso:
# Para abrir un long solo si el precio baja a 3000:
# abrir_orden_limit(client2()[0], "ETHUSDT", 0.01, 3000, side="BUY", leverage=10)
# Para abrir un short solo si el precio sube a 3500:
# abrir_orden_limit(client2()[0], "ETHUSDT", 0.01, 3500, side="SELL", leverage=10)

if __name__ == "__main__":
    abrir_long(client_api()[0], 'WLDUSDT', 1, leverage=10)