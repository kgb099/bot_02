import os
from binance.client import Client
from datetime import datetime, timedelta 
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv, set_key
DOTENV_PATH = ".env"

def client_api() -> Tuple[Client, str, str]:
    """
    Crea una instancia del cliente de Binance a partir de variables de entorno.

    Retorna:
    - Tuple: (cliente, API_KEY, API_SECRET)
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    client_api = Client(api_key, api_secret)
    return client_api, api_key, api_secret