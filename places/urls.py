from django.urls import path

from .views import *


urlpatterns = [
    path('', index),
    path('places/<int:id>/', place_view),
]
