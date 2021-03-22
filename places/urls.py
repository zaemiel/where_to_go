from django.urls import path

from .views import *


urlpatterns = [
    path('', index),
    path('places/<int:id>/', place_view),
    path('place/<str:place_id>/', place_detail_view)
]
