import requests
import config

def fetch_mbta_data(route_id):
    headers = {
        'x-api-key': config.MBTA_API_KEY
    }
    params = {
        'filter[route]': route_id,  # Specific route ID
    }
    response = requests.get('https://api-v3.mbta.com/predictions', headers=headers, params=params)
    return response.json()

def fetch_routes():
    headers = {
        'x-api-key': config.MBTA_API_KEY
    }

    response = requests.get('https://api-v3.mbta.com/routes', headers=headers)
    return response.json()
