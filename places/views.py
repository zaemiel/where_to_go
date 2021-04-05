from django.shortcuts import render
from django.shortcuts import get_object_or_404

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
                'coordinates': place.coordinates
            },
            'properties': {
                'id': place.id,
                'title': place.title,
                'detailsUrl': ''
            }
        }

        places_geojson['features'].append(place_geojson)

    return render(request, 'index.html', context={'places_geojson': places_geojson})


def place_view(request, id):
    place = get_object_or_404(Place, id=id)

    place_dict = model_to_dict(place)
    place_dict.update({
        'imgs': place.imgs,
    })
    return JsonResponse(place_dict, json_dumps_params={'ensure_ascii': False, 'indent': 2})
