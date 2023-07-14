from django.urls import path
from . import views

app_name = "combine_playlists"

urlpatterns = [
    path('', views.start, name='start'),
    path('complete/', views.complete, name='complete'),
]
