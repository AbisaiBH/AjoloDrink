from django.urls import path
from . import views

urlpatterns = [
    path('season', views.Season_cocktail, name='Season_cocktail'),
    path('cocktails', views.All_cocktail, name='All_cocktail'),
    path('register', views.Create_account, name='Create_account'),
    path('login', views.Login, name='Login'),
    path('logout', views.LogOut, name='LogOut'),
]