import json

import requests

import settings

keywords = json.loads(requests.get(settings.api_url + "/catalog/ability-words").text)["data"]