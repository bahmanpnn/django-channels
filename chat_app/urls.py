from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home-page'),
    path('chat/<str:room_name>/', room, name='room-page'),
]
