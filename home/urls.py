from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('city',views.func,name="mainfunction"),
    path('test',views.test,name="test"),
    path('search',views.search,name="search"),
    path("signup",views.signup_view,name="sign_up")
]