from django.shortcuts import render, redirect
import requests
from spotify_tools import config
from home.models import Token
import spotipy

def start(request):
    try:
        token=Token.objects.filter(user=request.user).first()
        sp = spotipy.Spotify(auth=token)
    except spotipy.client.SpotifyException:
        print("\n\n\nEntered\n\n\n")
        sp_auth = config.sp_auth
        new_token = sp_auth.refresh_access_token(token.refresh_token)
        token.access_token = new_token['access_token']
        token.refresh_token = new_token['refresh_token']
        sp = spotipy.Spotify(auth=token)

    premium = False
    if sp.current_user()['product'] == 'premium':
        premium = True
    return render(request, 'liked_to_playlists/start.html', {'premium': premium})


def run(request, index=None):

    sp = spotipy.Spotify(auth=Token.objects.filter(user=request.user).first())
    user_playlists = sp.current_user_playlists()['items']
    if index and int(index) > 0:
        sp.playlist_add_items(playlist_id=user_playlists[int(index)-1]['id'], items=[request.session["current_track"]])

    web_device = ''
    devices = sp.devices()['devices']
    for i in range(len(devices)):
        if devices[i]['name'].startswith('Web Player'):
            web_device = devices[i]['id']

    if web_device == '':
        return redirect("liked_to_playlists:start")
    else:
        if 'offset' not in request.session:
            request.session['offset'] = 0
        
        track = sp.current_user_saved_tracks(offset=request.session['offset'], limit=1)['items'][0]['track']
        sp.start_playback(web_device, uris=[track['uri']],position_ms=0)
        request.session["offset"] += 1
        request.session["current_track"] = track['uri']
        
        playlists = []
        for i in range(len(user_playlists)):
            playlists.append(user_playlists[i]['name'])
        context = {
            'track': track['name'],
            'uri': track['uri'],
            'artist': track['artists'][0]['name'],
            'image': track['album']['images'][0]['url'],
            'playlists': playlists,
        }
        return render(request, 'liked_to_playlists/run.html', context)

# If user wants to save progress, simply save the offset, use with added on value in return from current_user_saved_tracks to add new songs