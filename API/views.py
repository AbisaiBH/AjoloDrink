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
        objects_cocktails = list()
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
def Popular_cocktail(request):
    pass
    
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

## PENDING
@csrf_exempt
def Profile(request):
    pass

@csrf_exempt
def Create_account(request):
    pass

@csrf_exempt
def Login(request):
    pass
    