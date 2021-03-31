from django.db import models
from tinymce import models as tinymce_models
from django.utils.html import mark_safe


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    placeId = models.CharField(max_length=200, verbose_name='ID места')
    description_short = tinymce_models.HTMLField(blank=True, verbose_name='Короткое описание')
    description_long = tinymce_models.HTMLField(blank=True, verbose_name='Длинное описание')
    lat = models.FloatField(verbose_name='Широта')
    long = models.FloatField(verbose_name='Долгота')

    @property
    def coordinates(self):
        return self.lat, self.long

    @property
    def imgs(self):
        images_urls = [photo.url for photo in self.images.all()]
        return images_urls

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Image(models.Model):
    photo = models.ImageField(upload_to='places', verbose_name='Картинка')
    place = models.ForeignKey(Place, null=True, blank=True, related_name='images', on_delete=models.CASCADE)
    position = models.IntegerField(default=0, blank=False, verbose_name='Позиция')

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
