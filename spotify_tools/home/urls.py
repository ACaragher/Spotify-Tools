from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify_login', views.spotify_login, name='spotify-login'),
    path('spotify_login/complete', views.spotify_loggedin, name='spotify-loggedin')
]
