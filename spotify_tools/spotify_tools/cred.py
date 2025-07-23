import os

client_ID=os.getenv('SPOTIFY_CLIENT_ID')
client_SECRET=os.getenv('SPOTIFY_API_KEY')
redirect_uri='https://www.caragher.ie/social/complete/spotify/'
scope='app-remote-control streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'
