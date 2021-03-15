from django.shortcuts import render

from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import Place


def index(request):
    return render(request, 'index.html')


def place_view(request, place_id):
    place = Place.objects.get(placeId=place_id)

    place_dict = model_to_dict(place)
    place_dict.update({
        'imgs': place.imgs,
        'coordinates': place.coordinates
    })
    return JsonResponse(place_dict)
