import requests
from django.conf import settings

def fetch_from_tmdb(endpoint, params=None):
    
    api_key = settings.TMDB_API_KEY
    base_url = "https://api.themoviedb.org/3"
    if params is None:
        params = {}

    params['api_key'] = api_key
    params['language'] = 'es-MX'

    
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.get(url, params=params)
        print(f"DEBUG: Llamando a URL: {response.url}")
        response.raise_for_status() # Lanza error si la API falla
        return response.json()
    except Exception as e:
        print(f"Error conectando con TMDB: {e}")
        if response.status_code == 401:
            print("Error 401: Tu API Key no sirve.")
        return None