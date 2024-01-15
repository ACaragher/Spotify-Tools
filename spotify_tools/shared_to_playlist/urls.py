from django.urls import path
from . import views

app_name = "shared_to_playlist"

urlpatterns = [
    path('', views.start, name='start'),
    path('complete/', views.complete, name='complete'),
]
