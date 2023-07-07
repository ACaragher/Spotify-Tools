from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('social/', include('social_django.urls')),
    path('saved2playlists/', include('saved2playlists.urls')),
]
