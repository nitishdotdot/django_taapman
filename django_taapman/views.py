from django.shortcuts import render
from django.templatetags.static import static
from taapman_viewer.models import userInfo
import requests
def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user_object=userInfo.objects.get(email=email)
            if email==user_object.email and password==user_object.password:
                request.session['user_email']=user_object.email
                return render(request,'index.html')
            else:
                return render(request,'login.html',{'message':'incorrect!'})
        except Exception as ex:
            return render(request,'login.html',{'message':email+'\tdoes not exists!please sign up'})
    return render(request,'login.html')
def index(request):
    if request.session.get('user_email'):
        dataz={}
        if request.method=="POST":
            place=request.POST.get("place")
            try:
                 url=f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
                 headers = {
                  "User-Agent": "django_tapman (contact@nitish.com)",
                  "Accept-Language": "en" 
                  }
                 response=requests.get(url,headers=headers).json()[0]
                 lat=response['lat']
                 lon=response['lon']
                 full_address=response['display_name']
                 name=response['name']
                 address_type=response['addresstype']
                 country=full_address.split(',')[-1]
                 url=f"https://restcountries.com/v3.1/name/{country}"
                 response=requests.get(url,headers=headers).json()[0]
                 flag=response['flags'].get('png',static('not-found.avif'))
                 about_flag=response['flags'].get('alt','no description available')
                 languages=response['languages']
                 currency=response['currencies']
                 coatOfArms=response['coatOfArms'].get('png',static('not-found.avif'))
                 population=response['population']
                 capital=response['capital'][0]
                 land_locked=response['landlocked']
                 if land_locked:
                     land_locked="yes,It is LandLocked"
                 else:
                     land_locked="No,It is not LandLocked"
            
                 url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
                 response=requests.get(url,headers=headers).json()
                 date_x=[]
                 time_x=[]
                 temp=[]
                 for i in  response['hourly']['time']:
                     date_x.append(i[:10])
                     time_x.append(i[11:16])
                 for i in response['hourly']['temperature_2m']:
                     i=str(i)+"°C"
                     temp.append(i)
                 data=zip(date_x,time_x,temp)
                 list_data=list(data)
                 day1=list_data[:24]
                 day2=list_data[24:48]
                 day3=list_data[48:72]
                 day4=list_data[72:96]
                 day5=list_data[96:120]
                 day6=list_data[120:144]
                 day7=list_data[-24:]
                 dataz={'lat':lat,
                 'lon':lon,
                 'full_address':full_address,
                 'name':name,
                 'address_type':address_type,
                 'country':country,
                 'flag':flag,
                 'about_flag':about_flag,
                 'about_flag':about_flag,
                 'coatOfArms':coatOfArms,
                 'population':population,
                 'capital':capital,
                 'land_locked':land_locked
                    }
                 return render(request,'index.html',{'dataz':dataz,'day1':day1,'day2':day2,'day3':day3,'day4':day4,'day5':day5,'day6':day6,'day7':day7,'languages':languages,'currency':currency})
            except Exception as e:
                print(e)
                return render(request,'index.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')
def signup(request):
    if request.method=="POST":
        first_name=request.POST.get("f_name")
        last_name=request.POST.get("l_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        userInfo.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
        return render(request,'login.html')
    return render(request,"signup.html")
def logout(request):
    request.session.flush()
    return render(request,'login.html')
def about_me(request):
    return render(request,'about-me.html')
def about_developer(request):
    return render(request,'about-developer.html')

    
