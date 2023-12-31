from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify_login', views.spotify_login, name='spotify-login'),
    path('login_success', views.spotify_login_complete, name='spotify-login-complete'),
    path('logout', auth_views.LogoutView.as_view(template_name="home/logout.html"), name='logout'),
]
