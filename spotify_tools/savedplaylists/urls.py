from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('savedplaylists', views.login, name='login'),
    path('login/complete', views.loggedin, name='loggedin')
]
