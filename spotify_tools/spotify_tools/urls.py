from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('social/', include('social_django.urls')),
    path('liked_to_playlists/', include('liked_to_playlists.urls', namespace='liked_to_playlists')),
    path('setlist/', include('setlist.urls', namespace='setlist')),
    path('combine_playlists/', include('combine_playlists.urls', namespace='combine_playlists')),
]
