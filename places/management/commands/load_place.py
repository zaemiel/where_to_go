from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
from pathlib import Path
from time import time_ns

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from PIL import Image as pil_image
import requests

from places.models import Place, Image


def make_request(url):
    r = requests.get(url)
    r.raise_for_status()

    if not 'text/plain' in r.headers['Content-Type']:
        # image = pil_image.open(BytesIO(r.content))
        filename = url.split('/')[-1]
        image = ContentFile(r.content, name=filename)
        # image.filename =
        return image
    return r.json()

def rus_to_lat(sentence):
    rus_lat = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'g', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'x', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'ъ': '', 'ы': 'y',
        'ь': '', 'э': 'e', 'ю': 'u', 'я': 'ja'
    }

    transliterated = ''
    for letter in sentence.lower():
        if letter == ' ':
            transliterated += '_'
        else:
            transliterated += rus_lat.get(letter, letter)

    return transliterated


class PlaceJSON:
    def __init__(self, url):
        self.url = url
        self._read_json()

    def _read_json(self):
        content = make_request(self.url)

        self.title = content.get('title')
        self.description_short = content.get('description_short', '')
        self.description_long = content.get('description_long', '')
        # lat/long are mixed in jsons or in frontend part
        self.lat = content.get('coordinates').get('lng')
        self.lng = content.get('coordinates').get('lat')

        self._imgs = content.get('imgs')
        self.imgs = self._get_images()

        self.place_id = self._set_place_id()

    @property
    def coordinates(self):
        return self.lat, self.lng

    def _set_place_id(self):
        if self.title:
            return rus_to_lat(self.title)
        return str(time_ns())

    def _get_images(self):
        with ThreadPoolExecutor(len(self._imgs)) as executor:
            images = executor.map(make_request, self._imgs)

        return list(images)


class Command(BaseCommand):
    help = 'Loads places json data in to database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        place = PlaceJSON(options['url'])

        image_objects = []
        for image in place.imgs:
            image_obj = Image()
            image_obj.photo.save(image.name, image, save=True)
            image_objects.append(image_obj)

        new_place_obj, created = Place.objects.get_or_create(
            title=place.title,
            placeId=place.place_id,
            description_short=place.description_short,
            description_long=place.description_long,
            lat=place.lat,
            long=place.lng,
        )

        for image in image_objects:
            new_place_obj.images.add(image)

        new_place_obj.save()
