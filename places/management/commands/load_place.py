from concurrent.futures import ThreadPoolExecutor

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


def download_images(image_urls):
    with ThreadPoolExecutor(len(image_urls)) as executor:
        images = executor.map(download_image, image_urls)

    return list(images)


def get_serialized_place(url):
    response = requests.get(url)
    response.raise_for_status()
    content = response.json()

    image_urls = content.get('imgs', [])

    if image_urls:
        images = download_images(image_urls)
    else:
        images = []

    place_serialized = {
        'title': content['title'],
        'description_short': content.get('description_short', ''),
        'description_long': content.get('description_long', ''),
        # lat/long are mixed in jsons or in frontend part
        'lat': content['coordinates']['lng'],
        'lng': content['coordinates']['lat'],
        'imgs': images
    }

    return place_serialized


class Command(BaseCommand):
    help = 'Loads places json data in to database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        place = get_serialized_place(options['url'])

        place_obj, created = Place.objects.get_or_create(
            title=place['title'],
            lat=place['lat'],
            long=place['lng'],
        )

        place_obj.description_short = place.get('description_short')
        place_obj.description_long = place.get('description_long')

        for image in place.get('imgs'):
            image_obj = Image(place=place_obj)
            image_obj.photo.save(image.name, image, save=True)
            place_obj.images.add(image_obj)

        place_obj.save()
