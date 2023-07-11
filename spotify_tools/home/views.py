from django.shortcuts import render
from django.shortcuts import redirect

from spotify_tools import config


def index(request):
    return render(request, 'home/index.html')

def spotify_login(request):
    sp_auth = config.sp_auth
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

def spotify_login_complete(request):
    return render(request, 'home/index.html')
