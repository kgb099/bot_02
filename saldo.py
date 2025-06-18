from cliente_con_api import client_api

client = client_api()[0]
def obtener_saldo_usdt(client):
    """Devuelve el saldo de USDT dividido en 4 partes."""
    info_futuros = client.futures_account_balance()
    usdt_balance = next((item for item in info_futuros if item['asset'] == 'USDT'), None)
    saldo = float(usdt_balance['balance']) if usdt_balance else 0.0
    saldo = round(saldo, 2)
    return saldo

peso=[1, 2, 4, 8]

def calcular_partes_proporcionales(saldo_usdt, pesos=peso):
    """Calcula las 4 partes proporcionales del saldo según pesos [1, 2, 4, 8]."""
    cuarta_parte = saldo_usdt / 4
    if pesos is None:
        pesos = [1, 2, 4, 8]
    suma_pesos = sum(pesos)
    partes = [cuarta_parte * peso / suma_pesos for peso in pesos]
    return partes, cuarta_parte,pesos

def mostrar_resultados(partes, cuarta_parte, pesos):
    """Imprime los resultados en consola."""
    for i, parte in enumerate(partes, 1):
        print(f"Parte {i} (peso {pesos[i-1]}): {parte:.2f} USDT")
    print(f"Suma de las partes: {sum(partes):.2f} USDT")
    print(f"Saldo de la cuarta parte: {cuarta_parte:.2f} USDT")

def revisa_saldo(asset='USDT'):
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

def revisa_saldo_futuros(asset='USDT'):
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