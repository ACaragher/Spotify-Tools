from django.urls import path
from . import views

app_name = "tracks_to_playlists"

urlpatterns = [
    path('', views.select, name='select'),
    path('start', views.start, name='start'),
    path('run/', views.run, name='run'),
]
