import requests
from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from django.utils import timezone
from home.models import WeatherData
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from datetime import datetime
from home.models import UserSearch
import json
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def search(request):
    user = request.user
    print(user)
    recent_searches = UserSearch.objects.filter(username=user.username).order_by('-date')[:4]
    cities = [search.city for search in recent_searches]
    print(cities)
    return JsonResponse({'cities':cities})
@login_required   
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        print(request.user)
        session_id = request.session.session_key
        url='http://127.0.0.1:8000/search'
        headers = {
        'Cookie': f'sessionid={session_id}'
        }
        response=requests.get(url, headers=headers)
        rep=response.json()
        print(rep)
        return render(request,'index.html',rep)
def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,'login.html')
    return render(request,'login.html')
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            login(request, user)
            return redirect('/')
    return render(request, 'signup.html')
def logoutUser(request):
    logout(request)
    return redirect("/login")
@csrf_exempt
def test(request):
    if request.method=="POST":
        city = request.POST.get('city')
        today = datetime.today()
        api_key = '4874cd6008574fa584c25713241306'  # Replace with your actual API key
        base_url = 'http://api.weatherapi.com/v1/history.json'
        username = request.user.username
        current_date_time = timezone.now()
        # Get dates for the past three days
        three_days_ago = today - timedelta(days=3)
        WeatherData.objects.filter(date__lt=three_days_ago).delete()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 4)]
        weather_data = []
        for date_str in dates:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            weather_record = WeatherData.objects.filter(city=city, date=date_obj).first()
            
            if weather_record:
                weather_data.append({
                    'date': date_str,
                    'maxtemp_c': weather_record.maxtemp_c,
                    'mintemp_c': weather_record.mintemp_c,
                })
            else:
                response = requests.get(base_url, params={
                    'key': api_key,
                    'q': city,
                    'dt': date_str
                })
                
                if response.status_code == 200:
                    data = response.json()
                    if 'forecast' in data and 'forecastday' in data['forecast']:
                        forecast_day = data['forecast']['forecastday'][0]['day']
                        max_temp = forecast_day['maxtemp_c']
                        min_temp = forecast_day['mintemp_c']
                        weather_record = WeatherData(
                            city=city,
                            date=date_obj,
                            maxtemp_c=max_temp,
                            mintemp_c=min_temp
                        )
                        weather_record.save()
                        weather_data.append({
                            'date': date_str,
                            'maxtemp_c': max_temp,
                            'mintemp_c': min_temp,
                        })
                else:
                    return JsonResponse({'error': 'Failed to fetch weather data'}, status=response.status_code)
        return JsonResponse({'weather_data': weather_data, 'city': city})
    return HttpResponse(status=404)
    
def func(request):
    if request.method=="POST":
        data=request.POST
        api='http://127.0.0.1:8000/test'
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token}
        response = requests.post(api, data=data, headers=headers)
        city = request.POST.get('city')
        username = request.user.username
        current_date_time = timezone.now()
        try:
            rep = response.json()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Failed to decode JSON response from /test/'}, status=500)
        if response.status_code==200:
            existing_record = UserSearch.objects.filter(username=username, city=city).first()
            if existing_record:
                existing_record.date = current_date_time
                existing_record.save()
            else:
                UserSearch.objects.create(username=username, city=city, date=current_date_time)
            return render(request, "city.html", rep)
        else:
            return HttpResponse(status=400)
    return HttpResponse(status=404)
    