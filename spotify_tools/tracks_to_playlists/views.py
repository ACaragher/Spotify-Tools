from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from spotify_tools import config

# Determines how many tracks are retrieved at a time, max = 50
LIMIT = config.LIMIT

@login_required
def select(request):
    sp = config.get_user_auth(request.user)

    if sp.current_user()['product'] == 'premium':
            user_playlists = sp.current_user_playlists()['items']
            playlists = []
            for i in range(len(user_playlists)):
                playlists.append(user_playlists[i]['name'])
            return render(request, 'tracks_to_playlists/select.html', {'playlists': playlists, 'premium': True})
    else:
        return render(request, 'tracks_to_playlists/select.html', {'premium': False})
    
@login_required
def start(request):
    sp = config.get_user_auth(request.user)
     
    if sp.current_user()['product'] == 'premium':
        if request.method == 'POST':
            user_playlists = sp.current_user_playlists()['items']
            playlist_selected = request.POST.get('playlist_radio')
            if playlist_selected != 'liked':
                playlist_selected = user_playlists[int(playlist_selected)]['id']
            playlist_songs = []
            if playlist_selected == 'liked':
                playlist_songs = sp.current_user_saved_tracks(offset=0, limit=LIMIT)['items']
            else:
                playlist_songs = sp.user_playlist_tracks(playlist_id=playlist_selected, limit=LIMIT, offset=0, fields='items')['items']
            # Store each track in the session cache, clear any values that may remain from a previous use
            for i in range(LIMIT):
                if i < len(playlist_songs):
                    request.session[i] = playlist_songs[i]['track']
                elif str(i) in request.session.keys():
                    del request.session[str(i)]
            request.session["playlist"] = playlist_selected
            request.session["current_track"] = 0
            request.session["offset"] = 50
            request.session.save()
            return render(request, 'tracks_to_playlists/start.html', {'premium': True})
    else:
        return render(request, 'tracks_to_playlists/start.html', {'premium': False})


@login_required
def run(request):
    sp = config.get_user_auth(request.user)
 
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
            playlist_songs = []
            playlist_selected = request.session["playlist"]
            print(f"Playlist Selected: {playlist_selected}")
            if playlist_selected == "liked":
                playlist_songs = sp.current_user_saved_tracks(offset=request.session["offset"], limit=LIMIT)['items']
            else:
                playlist_songs = sp.user_playlist_tracks(playlist_id=playlist_selected, offset=request.session["offset"], limit=LIMIT, fields='items')['items']
                
            if playlist_songs:
                for i in range(len(playlist_songs)):
                    request.session[i] = playlist_songs[i]['track']
                request.session["current_track"] = 0
                request.session["offset"] += 50
            # i.e. if there are no more tracks left
            else:
                return render(request, 'tracks_to_playlists/complete.html')
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
        return render(request, "tracks_to_playlists/start.html", {'failure': True, 'premium': True}) 
    
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
    return render(request, 'tracks_to_playlists/run.html', context)