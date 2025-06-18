
from cliente_con_api import client_api
from binance.client import Client  # Asegurate de tener esta importación si usás tipado

client: Client = client_api()[0]

def obtener_saldo_usdt(client: Client) -> float:
    """
    Obtiene el saldo total de USDT en cuenta de futuros.

    Parámetros:
    - client (Client): Cliente autenticado de Binance.

    Retorna:
    - float: Saldo total disponible en USDT, redondeado a 2 decimales.
    """
    info_futuros = client.futures_account_balance()
    usdt_balance = next((item for item in info_futuros if item['asset'] == 'USDT'), None)
    saldo = float(usdt_balance['balance']) if usdt_balance else 0.0
    saldo = round(saldo, 2)
    return saldo

peso = [1, 2, 4, 8]

def calcular_partes_proporcionales(saldo_usdt: float, pesos: list[int] = peso) -> tuple[list[float], float, list[int]]:
    """
    Divide el saldo total en 4 partes proporcionales, según los pesos definidos.

    Parámetros:
    - saldo_usdt (float): Saldo total en USDT.
    - pesos (list[int], opcional): Lista de pesos para la distribución. Por defecto [1, 2, 4, 8].

    Retorna:
    - tuple: (lista de partes proporcionales, valor de una cuarta parte, lista de pesos utilizados).
    """
    cuarta_parte = saldo_usdt / 4
    if pesos is None:
        pesos = [1, 2, 4, 8]
    suma_pesos = sum(pesos)
    partes = [cuarta_parte * peso / suma_pesos for peso in pesos]
    return partes, cuarta_parte, pesos

def mostrar_resultados(partes: list[float], cuarta_parte: float, pesos: list[int]) -> None:
    """
    Muestra por consola las partes proporcionales calculadas.

    Parámetros:
    - partes (list[float]): Lista de montos en USDT correspondientes a cada peso.
    - cuarta_parte (float): Monto base de la cuarta parte del saldo.
    - pesos (list[int]): Lista de pesos usados en la distribución.
    """
    for i, parte in enumerate(partes, 1):
        print(f"Parte {i} (peso {pesos[i-1]}): {parte:.2f} USDT")
    print(f"Suma de las partes: {sum(partes):.2f} USDT")
    print(f"Saldo de la cuarta parte: {cuarta_parte:.2f} USDT")

def revisa_saldo(asset: str = 'USDT') -> float | None:
    """
    Revisa el saldo libre disponible en spot para un activo específico.

    Parámetros:
    - asset (str): Ticker del activo (por defecto 'USDT').

    Retorna:
    - float | None: Saldo libre disponible en cuenta spot, o None si no se encuentra.
    """
    try:
        account_info = client.get_account()
        usdt = next((b for b in account_info['balances'] if b['asset'] == asset), None)
        if usdt:
            return float(usdt['free'])
        else:
            print(f"No se encontró saldo para {asset}")
            return None
    except Exception as e:
        print(f"Error al obtener saldo: {e}")
        return None

def revisa_saldo_futuros(asset: str = 'USDT') -> float | None:
    """
    Revisa el saldo disponible en cuenta de futuros para un activo específico.

    Parámetros:
    - asset (str): Ticker del activo (por defecto 'USDT').

    Retorna:
    - float | None: Saldo disponible en futuros, o None si no se encuentra.
    """
    try:
        balances = client.futures_account_balance()
        item = next((b for b in balances if b['asset'] == asset), None)
        if item:
            return float(item['balance'])
        else:
            print(f"No se encontró saldo de futuros para {asset}")
            return None
    except Exception as e:
        print(f"Error al obtener saldo de futuros: {e}")
        return None
