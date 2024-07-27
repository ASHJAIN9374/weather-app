from django.contrib import admin
from home.models import WeatherData
from home.models import UserSearch
# Register your models here.
admin.site.register(WeatherData)
admin.site.register(UserSearch)