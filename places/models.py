from django.db import models
from tinymce import models as tinymce_models
from django.utils.html import mark_safe
from django.urls import reverse


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description_short = tinymce_models.HTMLField(blank=True, verbose_name='Короткое описание')
    description_long = tinymce_models.HTMLField(blank=True, verbose_name='Длинное описание')
    lat = models.FloatField(verbose_name='Широта')
    long = models.FloatField(verbose_name='Долгота')

    @property
    def coordinates(self):
        """
        GPS coordinates are represented as an [latitude, longitude] array.

        Latitude is a geographic coordinate that specifies the north–south position of a point on the Earth's surface (https://en.wikipedia.org/wiki/Latitude).

        Longitude is a geographic coordinate that specifies the east–west position of a point on the Earth's surface (https://en.wikipedia.org/wiki/Longitude).

        Thus the latitude is the position of the point on the Y-axis.
        And the longitude is the postition of the point on the X-axis.

        But in GeoJSON format the order of elements must follow x, y, z order (easting, northing, altitude for coordinates in a projected coordinate reference system, or longitude, latitude, altitude for coordinates in a geographic coordinate reference system).

        Source: https://geojson.org/geojson-spec.html#positions
        """
        return self.long, self.lat

    @property
    def imgs(self):
        images_urls = [photo.url for photo in self.images.all()]
        return images_urls

    def get_absolute_url(self):
        return reverse('place_details_url', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Image(models.Model):
    photo = models.ImageField(upload_to='places', verbose_name='Картинка')
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    position = models.IntegerField(default=0, verbose_name='Позиция')

    @property
    def url(self):
        return self.photo.url

    @property
    def thumbnail(self):
        if self.photo:
            return mark_safe(f'<img src="{self.url}" height="200">')

    def __str__(self):
        return str(self.photo)

    class Meta:
        ordering = ['position']
