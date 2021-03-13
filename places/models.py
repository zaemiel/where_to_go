from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField(blank=True, null=True)
    description_long = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['title']
