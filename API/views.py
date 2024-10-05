from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import http
import json
import ephem
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from .models import Cocktail
from django.core import serializers
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def Stations(tdy):
    year = tdy.year
    date = ephem.Date(tdy)
    seasons = {
        'Winter': ephem.Date(f'{year}-12-21'),
        'Spring': ephem.Date(f'{year}-03-20'),
        'Summer': ephem.Date(f'{year}-06-21'),
        'Fall': ephem.Date(f'{year}-09-23')
    }
    for season, start_date in sorted(seasons.items(), key=lambda x: x[1]):
        if date < start_date:
            break
        s = season
    season = Cocktail.get_season_value(s)
    return season
        
@csrf_exempt
def Season_cocktail(request):
    if request.method == 'GET':
        page = request.GET.get('page', None)
        if page is None:
            page = 1
        
        td_zone = datetime.now()
        station = Stations(td_zone)
        
        list_cocktails = Cocktail.objects.filter(season = station)
        print(f" se obtuvo el objeto {list_cocktails}")        
        objects_cocktails = list()
        for i, coctel in enumerate(list_cocktails):
            print(f" posicion {i} con el coctel: {coctel.name}")
            coctel_dict = {
                "id": coctel.uid,
                "image": coctel.image,
                "name": coctel.name,
                "tags": coctel.tags,
                "description": coctel.description,
                "Liquor": coctel.liquor,
                "lvl_alcohol": coctel.get_alcohol_lvl_display(),
                "season": coctel.get_season_display(),
                "review": 0,
            }
            objects_cocktails.append(coctel_dict)
        paginator = Paginator(objects_cocktails, 10)
        page_obj = paginator.get_page(page)
        
        data = {
        'pages': paginator.num_pages,
        'current_page': page,
        'data': list(page_obj)
        }

        return JsonResponse(data, safe=False, status=http.HTTPStatus.OK)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
@csrf_exempt
def Popular_cocktail(request):
    if request.method == 'GET':
        page = request.GET.get('page', None)
        if page is None:
            page = 1
        
        td_zone = datetime.now()
        
        # list_cocktails = Cocktail.objects.filter(season = station)    
        objects_cocktails = list()
        # 
        paginator = Paginator(objects_cocktails, 10)
        page_obj = paginator.get_page(page)
        
        data = {
        'pages': paginator.num_pages,
        'current_page': page,
        'data': list(page_obj)
        }
        
        return JsonResponse("No available cocktails", safe=False, status=http.HTTPStatus.OK)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)
    
@csrf_exempt
def All_cocktail(request):
    if request.method == 'GET':
        page = request.GET.get('page', None)
        if page is None:
            page = 1
        
        list_cocktails = Cocktail.objects.all()
        
        objects_cocktails = list()
        total_pages = 0
        for coctel in list_cocktails:
            coctel_dict = {
                "id": coctel.uid,
                "image": coctel.image,
                "name": coctel.name,
                "tags": coctel.tags,
                "description": coctel.description,
                "Liquor": coctel.liquor,
                "lvl_alcohol": coctel.get_alcohol_lvl_display(),
                "season": coctel.get_season_display(),
                "review": 0,
            }
            objects_cocktails.append(coctel_dict)
        paginator = Paginator(objects_cocktails, 10)
        page_obj = paginator.get_page(page)
        
        data = {
        'pages': paginator.num_pages,
        'current_page': page,
        'data': list(page_obj)
        }

        return JsonResponse(data, safe=False, status=http.HTTPStatus.OK)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)

@csrf_exempt
def Create_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        username = data.get('username')
        if not username:
            return JsonResponse({"error": "Missing username"}, status=400)
        email = data.get('email')
        if not email:
            return JsonResponse({"error": "Missing email"}, status=400)
        password = data.get('password')
        if not password:
            return JsonResponse({"error": "Missing password"}, status=400)
    
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
            
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse("User Created", safe=False, status=http.HTTPStatus.OK)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)
        
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    
        username = data.get('username')
        if not username:
            return JsonResponse({"error": "Missing username"}, status=400)

        password = data.get('password')
        if not password:
            return JsonResponse({"error": "Missing password"}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=200)
        else:
            return JsonResponse({"message": "Login successful"}, status=401)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)

@csrf_exempt
def LogOut(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "Logout successful"}, status=200)
        else:
            return JsonResponse({"error": "No user is currently logged in"}, status=400)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)
        
## PENDING
@csrf_exempt
def Profile(request):
    pass