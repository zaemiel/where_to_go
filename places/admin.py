from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['thumbnail']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'photo', 'thumbnail']
    readonly_fields = ['thumbnail']

    def thumbnail(self, obj):
        return obj.thumbnail

    thumbnail.short_description = 'Preview'
    thumbnail.allow_tags = True
