from indicadores.ind_emmas import obtener_smas_futuros
from indicadores.ind_adx import obtener_adx_futuros  # Debe devolver adx, plus_di, minus_di
from indicadores.ind_obv import calcular_obv_futuros
from indicadores.ind_Bandas_de_Bollinger import calcular_bollinger_futuros
from indicadores.ind_cci import calcular_cci_futuros

symbol = "ETHUSDT"  # Cambia a tu símbolo preferido

def puntaje_ema(sma10, sma55):
    if sma10.iloc[-1] > sma55.iloc[-1]:
        return 3  # Tendencia alcista
    elif sma10.iloc[-1] < sma55.iloc[-1]:
        return 1  # Tendencia bajista
    else:
        return 2  # Lateral

def puntaje_adx(adx, plus_di, minus_di):
    # 3 si ADX fuerte y +DI/-DI claros, 2 si solo ADX > 20, 1 si débil
    if adx > 25 and plus_di > minus_di:
        return 3
    elif adx > 20:
        return 2
    else:
        return 1

def puntaje_obv(obv):
    if obv.iloc[-1] > obv.iloc[-2]:
        return 3
    elif obv.iloc[-1] < obv.iloc[-2]:
        return 1
    else:
        return 2

def puntaje_bollinger(close, sup, inf):
    if close > sup.iloc[-1]:
        return 3
    elif close < inf.iloc[-1]:
        return 3
    elif close > sup.iloc[-1]*0.98 or close < inf.iloc[-1]*1.02:
        return 2
    else:
        return 1

def puntaje_cci(cci):
    if cci.iloc[-1] > 100 or cci.iloc[-1] < -100:
        return 3
    elif 50 < cci.iloc[-1] <= 100 or -100 <= cci.iloc[-1] < -50:
        return 2
    else:
        return 1

def evaluar_estrategia(symbol="BTCUSDT", interval="15m", limit=100):
    # EMA
    sma10, sma55 = obtener_smas_futuros(symbol, interval, limit)
    # ADX
    adx, plus_di, minus_di = obtener_adx_futuros(symbol, interval, limit)
    # CCI
    cci = calcular_cci_futuros(symbol, interval, limit)
    cci_actual = cci.iloc[-1]
    cci_prev = cci.iloc[-2]
    pendiente_cci = cci_actual - cci_prev

    #print(f"ADX={adx:.2f}, +DI={plus_di:.2f}, -DI={minus_di:.2f}, EMA10={sma10.iloc[-1]:.2f}, EMA55={sma55.iloc[-1]:.2f}, CCI={cci_actual:.2f}, Pendiente_CCI={pendiente_cci:.2f}")

    # Lógica de decisión
    if (
        adx > 25 and
        plus_di > minus_di and
        sma10.iloc[-1] > sma55.iloc[-1] and
        cci_actual > 0 and pendiente_cci > 0
    ):
        print("Señal de COMPRA (LONG) confirmada por todos los indicadores.")
        # Aquí colocarías la orden LONG y la cobertura SHORT
    elif (
        adx > 25 and
        minus_di > plus_di and
        sma10.iloc[-1] < sma55.iloc[-1] and
        cci_actual < 0 and pendiente_cci < 0
    ):
        print("Señal de VENTA (SHORT) confirmada por todos los indicadores.")
        # Aquí colocarías la orden SHORT y la cobertura LONG
    else:
        print("No operar: los indicadores no están alineados para una entrada segura.")

if __name__ == "__main__":
    evaluar_estrategia(symbol=symbol,interval="1m", limit=100)
    evaluar_estrategia(symbol=symbol,interval="5m", limit=100)
    evaluar_estrategia(symbol=symbol,interval="15m", limit=100)
    evaluar_estrategia(symbol=symbol,interval="30m", limit=100)
    evaluar_estrategia(symbol=symbol,interval="1h", limit=100)
    evaluar_estrategia(symbol=symbol,interval="4h", limit=100)
    evaluar_estrategia(symbol=symbol,interval="1d", limit=100)
