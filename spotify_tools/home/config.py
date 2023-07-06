from spotipy.oauth2 import SpotifyOAuth
from . import cred

scope='user-read-playback-state, user-modify-playback-state, user-read-currently-playing, user-library-modify, user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public'
sp_auth = SpotifyOAuth(scope = scope, client_id=cred.client_ID, client_secret=cred.client_SECRET, redirect_uri=cred.redirect_uri, show_dialog=True)