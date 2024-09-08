from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import http
import json
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from .models import Cocktail
from django.core import serializers

@csrf_exempt
def Season_cocktail(request):
    pass
    
@csrf_exempt
def Popular_cocktail(request):
    pass
    
@csrf_exempt
def All_cocktail(request):
    if request.method == 'GET':
        list_cocktails = Cocktail.objects.all()
        
        cktail = []
        for coctel in list_cocktails:
            coctel_dict = {
                "id": coctel.uid,
                "image": coctel.image,
                "name": coctel.name,
                "tags": coctel.tags,
                "description": coctel.description,
                "Liquor": coctel.liquor,
                "lvl_alcohol": coctel.alcohol_lvl,
                "review": 0,
            }
            cktail.append(coctel_dict)

        return JsonResponse(cktail, safe=False, status=http.HTTPStatus.OK)
    else:
        return JsonResponse({'message': ("METHOD_NOT_ALLOWED")},
                            status=http.HTTPStatus.METHOD_NOT_ALLOWED)
        
@csrf_exempt
def Profile(request):
    pass

@csrf_exempt
def Create_account(request):
    pass

@csrf_exempt
def Login(request):
    pass
    