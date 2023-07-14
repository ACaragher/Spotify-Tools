from django.urls import path
from . import views

app_name = 'setlist'

urlpatterns = [
    path('', views.start, name='start'),
]
