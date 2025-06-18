import time
from datetime import datetime

def esperar_cierre_vela(intervalo="1m"):
    """
    Espera pasivamente hasta el cierre de la vela actual.
    Soporta intervalos: '1m', '5m', '15m', '30m', '1h', '4h', '1d'
    """
    ahora = datetime.utcnow()
    if intervalo == "1m":
        segundos_espera = 60 - ahora.second
    elif intervalo == "5m":
        segundos_espera = 60 * (5 - (ahora.minute % 5)) - ahora.second
    elif intervalo == "15m":
        segundos_espera = 60 * (15 - (ahora.minute % 15)) - ahora.second
    elif intervalo == "30m":
        segundos_espera = 60 * (30 - (ahora.minute % 30)) - ahora.second
    elif intervalo == "1h":
        segundos_espera = 60 * (60 - ahora.minute) - ahora.second
    elif intervalo == "4h":
        minutos_restantes = 60 * (4 - (ahora.hour % 4)) - ahora.minute
        segundos_espera = 60 * minutos_restantes - ahora.second
    elif intervalo == "1d":
        minutos_restantes = 60 * (24 - ahora.hour - 1) + (60 - ahora.minute)
        segundos_espera = 60 * minutos_restantes - ahora.second
    else:
        raise ValueError("Intervalo no soportado")
    if segundos_espera > 0:
        time.sleep(segundos_espera)
