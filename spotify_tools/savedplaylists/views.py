from django.shortcuts import render
import spotipy
from django.shortcuts import redirect
from . import config

def index(request):
    return render(request, 'savedplaylists/index.html')

def login(request):
    sp_auth = config.sp_auth
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

def loggedin(request):
    sp_auth = config.sp_auth
    auth_code = request.GET['code']
    access_token = sp_auth.get_access_token(code=auth_code)
    sp = spotipy.Spotify(auth=access_token['access_token'])
    return render(request, 'savedplaylists/loggedin.html')