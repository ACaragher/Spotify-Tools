from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect

def index(request):
    return render(request, 'savedplaylists/index.html')

def login(request):
    scope='user-read-playback-state, user-modify-playback-state, user-read-currently-playing, user-library-modify, user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public'
    sp_auth = SpotifyOAuth(
        scope = scope,
        client_id='0c5dc9ea1d5141799dd8d93e0ab7d81f',
        client_secret='216ac35f5bf94802a0064d031daf987c',
        redirect_uri='http://localhost:8000/login/complete',
        show_dialog=True
    )
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

def loggedin(request):
    return render(request, 'savedplaylists/loggedin.html')