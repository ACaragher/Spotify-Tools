from django.urls import path
from . import views

app_name = "liked_to_playlists"

urlpatterns = [
    path('', views.start, name='start'),
    path('run/', views.run, name='run'),
    path('run/<index>', views.run, name='run'),
]
