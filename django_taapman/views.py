from django.shortcuts import render
from django.templatetags.static import static
from taapman_viewer.models import userInfo
import requests


def index(request):
    place = request.POST.get("place")
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
        headers = {
            "User-Agent": "django_tapman (contact@nitish.com)",
            "Accept-Language": "en",
        }
        response = requests.get(url, headers=headers).json()[0]
        lat = response["lat"]
        lon = response["lon"]
        full_address = response["display_name"]
        name = response["name"]
        address_type = response["addresstype"]
        country = full_address.split(",")[-1].strip()
        url = f"https://api.restcountries.com/countries/v5/names.common/{country}"
        headers1 = {
            "User-Agent": "django_tapman (contact@nitish.com)",
            "Accept-Language": "en",
            "Authorization": "bearer rc_live_427bccdcde4348aeab5fee0a3887b53e",
        }
        response = requests.get(url, headers=headers1).json()["data"]["objects"][0]

        flag = response["flag"].get("url_png", static("not-found.avif"))

        about_flag = response["flag"].get("description", "no description available")

        languages = response["languages"][0]
        currency = response["currencies"]
        print(currency)
        # coatOfArms = response["coatOfArms"].get("png", static("not-found.avif"))
        population = response["population"]
        capital = response["capitals"][0]["name"]
        print(capital)
        land_locked = response["descriptions"]["short"]
        print(land_locked)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        response = requests.get(url, headers=headers).json()
        date_x = []
        time_x = []
        temp = []
        for i in response["hourly"]["time"]:
            date_x.append(i[:10])
            time_x.append(i[11:16])
        for i in response["hourly"]["temperature_2m"]:
            i = str(i) + "°C"
            temp.append(i)
        data = zip(date_x, time_x, temp)
        list_data = list(data)
        day1 = list_data[:24]
        day2 = list_data[24:48]
        day3 = list_data[48:72]
        day4 = list_data[72:96]
        day5 = list_data[96:120]
        day6 = list_data[120:144]
        day7 = list_data[-24:]
        dataz = {
            "lat": lat,
            "lon": lon,
            "full_address": full_address,
            "name": name,
            "address_type": address_type,
            "country": country,
            "flag": flag,
            "about_flag": about_flag,
            "about_flag": about_flag,
            "population": population,
            "capital": capital,
            "land_locked": land_locked,
        }
        return render(
            request,
            "index.html",
            {
                "dataz": dataz,
                "day1": day1,
                "day2": day2,
                "day3": day3,
                "day4": day4,
                "day5": day5,
                "day6": day6,
                "day7": day7,
                "languages": languages,
                "currency": currency,
            },
        )
    except Exception as e:
        print(e)
        return render(request, "index.html")


def about_me(request):
    return render(request, "about-me.html")


def about_developer(request):
    return render(request, "about-developer.html")
