from concurrent.futures import ThreadPoolExecutor
import json

from pathlib import Path
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

import requests

from places.models import Place, Image


def download_image(url):
    r = requests.get(url)
    r.raise_for_status()

    filename = Path(urlparse(url).path).name
    image = ContentFile(r.content, name=filename)
    return image


class PlaceJSON:
    def __init__(self, url):
        self.url = url
        self._read_json()

    def _read_json(self):
        response = requests.get(self.url)
        response.raise_for_status()
        content = response.json()

        self.title = content.get('title')
        self.description_short = content.get('description_short', '')
        self.description_long = content.get('description_long', '')
        # lat/long are mixed in jsons or in frontend part
        self.lat = content.get('coordinates').get('lng')
        self.lng = content.get('coordinates').get('lat')

        self._imgs = content.get('imgs')
        self.imgs = self._get_images()

    @property
    def coordinates(self):
        return self.lat, self.lng

    def _get_images(self):
        with ThreadPoolExecutor(len(self._imgs)) as executor:
            images = executor.map(download_image, self._imgs)

        return list(images)


class Command(BaseCommand):
    help = 'Loads places json data in to database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        place = PlaceJSON(options['url'])

        place_obj, created = Place.objects.get_or_create(
            title=place.title,
            lat=place.lat,
            long=place.lng,
        )

        for image in place.imgs:
            image_obj = Image(place=place_obj)
            image_obj.photo.save(image.name, image, save=True)
            place_obj.images.add(image_obj)

            place_obj.description_short = place.description_short
            place_obj.description_long = place.description_long

        place_obj.save()
