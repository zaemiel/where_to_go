from django.core import serializers
from django.shortcuts import render

from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import Place


def index(request):
    places_geojson = {
        'type': 'FeatureCollection',
        'features': []
    }

    for place in Place.objects.all():
        place_geojson = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lat, place.long]
            },
            'properties': {
                'title': place.title,
                'placeId': place.placeId,
                'detailsUrl': ''
            }
        }

        places_geojson['features'].append(place_geojson)

    return render(request, 'index.html', context={'places_geojson': places_geojson})


def place_view(request, place_id):
    place = Place.objects.get(placeId=place_id)

    place_dict = model_to_dict(place)
    place_dict.update({
        'imgs': place.imgs,
    })
    return JsonResponse(place_dict)
