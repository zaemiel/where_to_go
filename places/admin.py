from django.contrib import admin

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['thumbnail']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'thumbnail']
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        return obj.thumbnail

    thumbnail.short_description = 'Preview'
    thumbnail.allow_tags = True
