
import asyncio
import threading
from cliente_con_api import client_api 
from saldo import obtener_saldo_usdt, calcular_partes_proporcionales, mostrar_resultados, revisa_saldo, revisa_saldo_futuros
from apis import verificacion_la_expiracion,api_key_y_api_secret, modificar_apis_now
from long_short import abrir_long, abrir_short, operar_con_cobertura, calcular_cobertura
from telegram02 import enviar_varios_mensajes
from indicadores.ind_emmas import validar_cruce_medias
from precio import obtener_precio_actual
from tiempo_0 import esperar_cierre_vela

client = client_api()[0]
symbol = "ETHUSDT"  # Símbolo a operar
interval = "1m"  # Intervalo de tiempo para las medias móviles
limit = 100 # Número de velas a considerar para el cálculo de medias móviles
apalancamiento = 20  # Apalancamiento para las operaciones

def tel(texto):
    """
    Función para enviar un mensaje de texto a través del bot de Telegram.
    """
    try:
        asyncio.run(enviar_varios_mensajes([texto], espera=10))
    except Exception as e:
        print(f"Hilo Telegram Error al enviar mensaje: {e}")


def main():
    # Modificar las API keys si es necesario
    resultado = verificacion_la_expiracion()
    texto = str(revisa_saldo_futuros(asset='USDT'))
    precio_entrada=obtener_precio_actual(client=client_api()[0], symbol=symbol)
    cantidad = 0.01  # Cantidad a operar
    texto = (
            f"[🔔 INICIANDO BOT DE TRADING]\n"
            f"saldo de futuros: {texto}\n"
            f"[🟢 APERTURA LONG]\n"
            f"Tiker: {symbol}\n"
            f"precio de entrada: {precio_entrada}\n"
            f"cantidad: {cantidad}\n"
            f"operacion en usdt: {round( cantidad * precio_entrada)}\n"
            f"apalancamiento: {apalancamiento}x\n"
            f"cobertura Distance: {calcular_cobertura(precio_entrada, apalancamiento,tipo="long")['distancia_porcentual']}%\n"
            f"cobertura Target Price: {calcular_cobertura(precio_entrada, apalancamiento,tipo="long")['precio_objetivo']}\n")
    print(texto)
    hilo = threading.Thread(target=tel, args=(texto,))
    hilo.start()
    if not resultado:
        modificar_apis_now()
    saldo_usdt = obtener_saldo_usdt(client)
    partes, cuarta_parte, pesos = calcular_partes_proporcionales(saldo_usdt,pesos=[1, 2, 4, 8])
    mostrar_resultados(partes, cuarta_parte, pesos)
    print(revisa_saldo(asset='USDT'))

    while True:
        esperar_cierre_vela(intervalo=interval)
        resultado = validar_cruce_medias(symbol=symbol, interval=interval, limit=limit)
        print(resultado)

        if "alcista" in resultado.lower():
            operar_con_cobertura(client=client, symbol=symbol, direccion="long", apalancamiento=apalancamiento, porcentaje_riesgo=0.10, porcentaje_cobertura=0.01)
        elif "bajista" in resultado.lower():
            operar_con_cobertura(client=client, symbol=symbol, direccion="short", apalancamiento=apalancamiento, porcentaje_riesgo=0.10, porcentaje_cobertura=0.01)
        else:
            print("Sin señal clara, no se opera.")

     

if __name__ == "__main__":
    main()
