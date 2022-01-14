import os

class DefaultConfig:
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    #Create a LUIS App using the JSON provided in data folder. copy the LUIS app URL in LUIS_APP_URL value. 
    #Follw instructions given in the readme file.
    LUIS_APP_URL = ""
