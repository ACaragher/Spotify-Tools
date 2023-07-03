import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import webbrowser
import os

scope='user-read-playback-state, user-modify-playback-state, user-read-currently-playing, user-library-modify, user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))


# Get id of web player device
devices = sp.devices()['devices']
web_device = ''
while web_device == '':
    for i in range (len(devices)):
        if devices[i]['name'].startswith('Web Player'):
            web_device = devices[i]['id']
    # If there isn't a web player tab already open, open one
    # Else it will play music on already open web player
    if web_device == '':
        webbrowser.get('windows-default').open('https://open.spotify.com/collection/tracks')

# Get all of the user's playlists
user = sp.current_user()
playlists = sp.user_playlists(user['id'])['items']

# Create a string of all playlists enumerated that can be then printed out
playlist_str = ""
for i in range(len(playlists)):
    curr_playlsit =  "["+ str(i + 1) + "] " + playlists[i]['name'] + "\n"
    playlist_str += curr_playlsit

# Loop through each track in liked songs
next = " "
curr_offset = 0
while next:
    # Get next 50 tracks (50 is the max number of tracks that can be retreived per call)
    saved_songs = sp.current_user_saved_tracks(offset=curr_offset, limit=50)
    next = saved_songs['next']
    for i in range(len(saved_songs)):
            valid = False

            # Print track's name, artist, and play song
            track = saved_songs['items'][i]['track']
            artist = track['artists'][0]['name']
            sp.start_playback(web_device, uris=[track['uri']])

            # Get input from user, repeat until valid input received
            while not valid:
                print(f"\nTrack - '{track['name']}'\nArtist - '{artist}'\n")
                playlist = input(f"Which playlist should this song be put in?:\n{playlist_str}\n")
                print('-' * os.get_terminal_size().columns) # Print dashed line to console
                if str.lower(playlist) == 'skip' or str.lower(playlist) == 'stop':
                    valid = True
                # Input validation
                elif playlist.isdigit() and int(playlist) <= len(playlists) and int(playlist) > 0:
                    sp.playlist_add_items(playlist_id=playlists[int(playlist) - 1]['id'], items=[track['uri']]) # Add track to desired playlist
                    valid = True
                else:
                    print(f"\nInvalid input, please enter a number between 0 and {len(playlists)}")
            if str.lower(playlist) == 'stop':
                next = False
                break
            
    curr_offset += 50
    