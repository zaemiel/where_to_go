from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200)
    placeId = models.CharField(max_length=200, null=True)
    description_short = models.TextField(blank=True, null=True)
    description_long = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    long = models.FloatField()

    @property
    def coordinates(self):
        return self.lat, self.long

    @property
    def imgs(self):
        images_urls = [photo.url for photo in self.images.all()]
        return images_urls

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['title']


class Image(models.Model):
    photo = models.ImageField(upload_to='places', max_length=250)
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)

    @property
    def url(self):
        return self.photo.url

    def __str__(self):
        return str(self.photo)

    class Meta:
        ordering = ['photo']
