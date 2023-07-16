from django.urls import path
from . import views

app_name = "genre_to_playlist"

urlpatterns = [
    path('', views.start, name='start'),
    path('run/', views.run, name='run'),
    path('complete/', views.complete, name='complete'),
]
