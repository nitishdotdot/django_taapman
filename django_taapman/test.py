import requests
 
headers = {
            "User-Agent": "MyAppName/1.0 (your@email.com)"
        }
lat=68
lon=95
url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
response=requests.get(url,headers=headers).json()
data_time=[]
temp=[]
for i in  response['hourly']['time']:
    data_time.append(i)
for i in response['hourly']['temperature_2m']:
    temp.append(i)
data=zip(data_time,temp)
 