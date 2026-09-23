import requests
import json

country = "nepal"
url = f"https://api.restcountries.com/countries/v5/names.common/{country}"
headers1 = {"Authorization": "bearer rc_live_427bccdcde4348aeab5fee0a3887b53e"}
response = requests.get(url, headers=headers1)
print(response.json()["data"]["objects"][0]["flag"]["url_png"])
