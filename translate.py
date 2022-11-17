import configparser
import requests


def translateT(text: list) -> str:
    wd = ""
    
    config = configparser.ConfigParser()
    config.read(wd + '.env')
    key = config["section"]["API_KEY"]
    query = {"target_lang": "DE",
             "auth_key": key,
             "text": text,
             "source_lang": "EN"}
    url = "https://api-free.deepl.com/v2/translate"
    response = requests.post(url=url, data=query)
    return response.json()["translations"]
