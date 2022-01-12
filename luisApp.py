from config import DefaultConfig
import json
import requests

def getLuisResponse(query):
    CONFIG = DefaultConfig()

    url = CONFIG.LUIS_APP_URL
    url = url + '"' + query + '"'
    print(url)
    response = requests.get(url)
    data = response.json()

    return data
