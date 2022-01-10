import json

import requests

from src.settings.settings import api_url

keywords = json.loads(requests.get(api_url + "/catalog/ability-words").text)["data"]