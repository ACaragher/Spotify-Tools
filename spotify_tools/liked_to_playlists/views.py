from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Token
import spotipy

# Determines how many tracks are retrieved at a time, max = 50
LIMIT = 50

@login_required
def start(request):

    token=Token.objects.filter(user=request.user).first()
    sp = spotipy.Spotify(auth=token)

    if sp.current_user()['product'] == 'premium':
        liked_songs = sp.current_user_saved_tracks(offset=0, limit=LIMIT)['items']
        for i in range(len(liked_songs)):
            request.session[i] = liked_songs[i]['track']
        request.session["current_track"] = 0
        request.session["offset"] = 50
        request.session.save()
        return render(request, 'liked_to_playlists/start.html', {'premium': True})
    else:
        return render(request, 'liked_to_playlists/start.html', {'premium': False})

# Loops through each song in the user's liked songs
@login_required
def run(request):

    sp = spotipy.Spotify(auth=Token.objects.filter(user=request.user).first())
    user_playlists = sp.current_user_playlists()['items']

    track_key = request.session["current_track"]
    track = request.session[str(track_key)]
    # i.e. if not the first track
    if request.method == 'POST':
        # Add the song to the chosen playlist
        if 'skip' not in request.POST:
            index = request.POST.get("playlist", "")
            if int(index) >= 0:
                sp.playlist_add_items(playlist_id=user_playlists[int(index)-1]['id'], items=[track['uri']])      
        del request.session[str(track_key)]
        
        # Stores 50 (LIMIT) tracks in the session cache, removing a track when it has been interacted with
        # Once all 50 have been interacted with, retrieve the next 50
        if str(int(track_key) + 1) not in request.session.keys():
            liked_songs = sp.current_user_saved_tracks(offset=request.session["offset"], limit=LIMIT)['items']
            if liked_songs:
                for i in range(len(liked_songs)):
                    request.session[i] = liked_songs[i]['track']
                request.session["current_track"] = 0
                request.session["offset"] += 50
            # i.e. if there are no more tracks left
            else:
                render(request, 'liked_to_playlist/complete.html')
        else:
            request.session["current_track"] = int(track_key) + 1  
            track = request.session[str(int(track_key) + 1)]
    
    # Audio played through the web player. Retreives the web player id and makes sure that it is active
    web_device = ''
    devices = sp.devices()['devices']
    for i in range(len(devices)):
        if devices[i]['name'].startswith('Web Player'):
            web_device = devices[i]['id']

    if web_device == '':
        return render(request, "liked_to_playlists/start.html", {'failure': True, 'premium': True}) 
    
    sp.start_playback(web_device, uris=[track['uri']],position_ms=0)
    # Add each playlist to a list to be passed to the template
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