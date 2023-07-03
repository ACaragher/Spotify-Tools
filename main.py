import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import webbrowser
from playlist import saved_to_playlists

scope='user-read-playback-state, user-modify-playback-state, user-read-currently-playing, user-library-modify, user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))


# Get id of web player device
web_device = ''
webbrowser.get('windows-default').open('https://open.spotify.com/collection/tracks')
while web_device == '':
    # Spotify must be active on web device for it to appear on API response
    # Wait till user has played the song and device id has been obtained
    input("Play any song on Spotify to activate device, then press enter:\n")
    devices = sp.devices()['devices']
    for i in range (len(devices)):
        if devices[i]['name'].startswith('Web Player'):
            web_device = devices[i]['id']

saved_to_playlists(sp, web_device)