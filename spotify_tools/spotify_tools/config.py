from spotipy.oauth2 import SpotifyOAuth
import spotipy
from home.models import Token
from . import cred

# Determines how many tracks are retrieved at a time, max = 50
LIMIT = 50

def get_user_auth(user):
    sp = spotipy.Spotify(auth=Token.objects.filter(user=user).first())

    try:
        sp.current_user()  
    except spotipy.client.SpotifyException:
        print("Refreshing Spotify access_token...")
        sp_oauth = SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_uri, scope=cred.scope)
        user_token = Token.objects.filter(user=user).first()
        user_token.refresh_access_token(sp_oauth=sp_oauth)
        print("Access_token successfully refreshed")
        sp = spotipy.Spotify(user_token)
    return sp