from django.urls import path

from .views import index, place_view


urlpatterns = [
    path('', index),
    path('place/<str:place_id>/', place_view)
]
