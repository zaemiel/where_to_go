from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    placeId = models.CharField(max_length=200, verbose_name='ID места')
    description_short = models.TextField(blank=True, verbose_name='Короткое описание')
    description_long = models.TextField(blank=True, verbose_name='Длинное описание')
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
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    position = models.IntegerField(default=1, blank=True, verbose_name='Позиция')

    @property
    def url(self):
        return self.photo.url

    def __str__(self):
        return str(self.photo)

    class Meta:
        ordering = ['position']
