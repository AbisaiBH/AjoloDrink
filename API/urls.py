from django.urls import path
from . import views

urlpatterns = [
    path('season/', views.Season_cocktail, name='season'),
    path('cocktails/', views.All_cocktail, name='cocktails'),  
]