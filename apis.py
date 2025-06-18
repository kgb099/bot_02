from datetime import datetime, timedelta
from dotenv import set_key, load_dotenv
import os
import time
load_dotenv()  # Carga las variables de entorno desde el archivo .env
DOTENV_PATH = ".env"

def verificacion_la_expiracion():
    """
    Obtiene la fecha de expiracion de la clave del archivo de configuracion de entorno (ej: .env).
    - Si no se encuentra se indica el mensaje. \n
    Se compara la fecha de expiracion de la clave con la fecha actual.
    - Si supera o no (vence) se indica el mensaje respectivo. \n
    :return: (texto, resultado) -> tuple
    """
    print("verificando la expiracion de las apis...")
    expiracion_str = os.getenv("expiracion")
    if not expiracion_str:
        return "No se encontró la variable de entorno 'expiracion'", False

    expiracion = datetime.strptime(expiracion_str, "%d-%m-%Y")
    now = datetime.now()

    if expiracion <= now:
        return "hay que cambiar las apis", False

    return "las apis estan correctas", True

def api_key_y_api_secret():
    """
    Obtiene la api key y api secret del archivo de configuracion de entorno (ej: .env).
    :return: api_key y api_secret -> tuple
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    return (api_key, api_secret)


def modificar_apis_now() -> tuple:
    """
    Compara fecha de expiracion de apis con la fecha actual si estan dentro del rango de 28 dias.
    - Si no cumple (vence) se solicita al usuario las nuevas api key y secret.\n
    Se comparan las nuevas apis con las recien vencidas.
    - Si no son iguales se guardan en el archivo de configuracion de entorno (ej: .env). \n
    :return: api_key_now, api_secret_now -> tuple
    """
    api_key_vieja = api_key_y_api_secret()[0]
    api_secret_vieja = api_key_y_api_secret()[1]
    fecha_de_expiracion = datetime.now() + timedelta(days=28)
    fecha_de_expiracion = fecha_de_expiracion.strftime("%d-%m-%Y")

    def cargar_nuevas_apis():
        return input("cargar api key nueva: \n"), input("cargar api secret nueva: \n")

    api_key_now, api_secret_now = cargar_nuevas_apis()
    if api_key_now == api_key_vieja or api_secret_now == api_secret_vieja:
        compare_apis = True
        while compare_apis:

            print(
                "Ambas claves deben ser diferentes de las actuales. \nPor favor, ingrese nuevas claves."
            )

            api_key_now, api_secret_now = cargar_nuevas_apis()
            compare_apis = api_key_now == api_key_vieja
            if not compare_apis:
                compare_apis = api_secret_now == api_secret_vieja

    # Si llega aca contamos con api key y api secret nuevas y distantas a las anteriores
    def save_api_key_y_api_secret(env_file=DOTENV_PATH):
        try:
            set_key(env_file, "API_KEY", api_key_now)
            set_key(env_file, "API_SECRET", api_secret_now)
            set_key(env_file, "creacion", datetime.now().strftime("%d-%m-%Y"))
            set_key(env_file, "experacion", fecha_de_expiracion)
            return (api_key_now, api_secret_now)
        except Exception as set_key_exception:
            return set_key_exception

    save_apis = save_api_key_y_api_secret(DOTENV_PATH)
    while type(save_apis) is Exception:
        print("Error saving api key y api_secret: ", save_apis)
        file_not_found_error = ""
        # resuelve error de archivo de configuracion
        if str(save_apis).__contains__(file_not_found_error):
            save_apis = save_api_key_y_api_secret(
                input("por favor indica el archivo de configuracion (ej: .env) \n-> ")
            )
            continue
        # reintento
        time.sleep(5)
        save_apis = save_api_key_y_api_secret(DOTENV_PATH)

    print("Ambas claves han sido actualizadas con éxito.")
    return save_apis

if __name__ == "__main__":
    texto, resultado = verificacion_la_expiracion()
    print(texto)
    if not resultado:
        modificar_apis_now()