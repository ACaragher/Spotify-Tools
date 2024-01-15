from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('social/', include('social_django.urls')),
    path('tracks_to_playlists/', include('tracks_to_playlists.urls', namespace='tracks_to_playlists')),
    path('shared_to_playlist/', include('shared_to_playlist.urls', namespace='shared_to_playlist')),
    path('combine_playlists/', include('combine_playlists.urls', namespace='combine_playlists')),
    path('genre_to_playlist', include('genre_to_playlist.urls', namespace='genre_to_playlist'))
]
