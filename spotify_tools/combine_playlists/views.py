from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from spotify_tools import config

# Determines how many tracks are retrieved at a time, max = 50
LIMIT = config.LIMIT

def start(request):
    sp = config.get_user_auth(request.user)
 
    if sp.current_user()['product'] == 'premium':
        user_playlists = sp.current_user_playlists()['items']
        playlists = []
        for i in range(len(user_playlists)):
            playlists.append(user_playlists[i]['name'])
        return render(request, 'combine_playlists/start.html', {'playlists': playlists, 'premium': True})
    return render(request, 'combine_playlists/start.html', {'premium': False})

@login_required
def complete(request):
    sp = config.get_user_auth(request.user)
 
    user_playlists = sp.current_user_playlists()['items']
    if request.method == 'POST':
        playlist_checkbox = request.POST.getlist('playlist_checkbox')
        playlist_selection = request.POST.getlist('playlist_select')[0]
        new_playlist = request.POST.get('new_playlist')
        selected_ids = []
        if playlist_checkbox != "":
            for playlist in playlist_checkbox:
                # Get list of id of each playlist selected
                if playlist == 'liked':
                    selected_ids.append('liked')
                else:
                    selected_ids.append(user_playlists[int(playlist)]['id'])
            # If user chose an existing playlist
            if 'current_playlist_btn' in request.POST and playlist_selection != "":
                if playlist_selection in playlist_checkbox: playlist_checkbox.remove(playlist_selection)
                # Get playlist id where results of playlist combination will be put
                destination_id = user_playlists[int(playlist_selection)]['id']
                combine_playlists(selected_ids, destination_id, request.user, sp)
                return render(request, 'combine_playlists/complete.html')
            elif 'new_playlist_btn' in request.POST:
                # Create a new playlist prior to combining
                new_playlist = sp.user_playlist_create(user=request.user, name=new_playlist)['id']
                combine_playlists(selected_ids, new_playlist, request.user, sp)
                return render(request, 'combine_playlists/complete.html')
            else:
                playlists = []
                for i in range(len(user_playlists)):
                    playlists.append(user_playlists[i]['name'])
                error_text = "Select a playlist to copy to or enter a name to create a new playlist"
        else:
            playlists = []
            for i in range(len(user_playlists)):
                playlists.append(user_playlists[i]['name'])
            error_text = "Please select which playlists you wish to copy"
        return render(request, 'combine_playlists/start.html', {"premium": True, "error": True, "error_text": error_text, "playlists": playlists})
        
def combine_playlists(selected_playlists, destination_playlist, user, sp):
    for playlist_id in selected_playlists:
        offset = 0
        try:
            if playlist_id == 'liked':
                curr_iter_songs = sp.current_user_saved_tracks(offset=offset, limit=LIMIT)['items']
            else:
                curr_iter_songs = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=0)['items']
            tracks = [track['track']['uri'] for track in curr_iter_songs]
            sp.user_playlist_add_tracks(user=user, playlist_id=destination_playlist, tracks=tracks)

            while curr_iter_songs:
                if playlist_id == 'liked':
                    offset += 50
                    curr_iter_songs = sp.current_user_saved_tracks(offset=offset, limit=LIMIT)['items']
                else:
                    offset += 100
                    curr_iter_songs = sp.user_playlist_tracks(user=user, offset=offset, limit=100, playlist_id=playlist_id)['items']
                tracks = [track['track']['uri'] for track in curr_iter_songs]
                sp.user_playlist_add_tracks(user=user, playlist_id=destination_playlist, tracks=tracks)

        except Exception as e:
            print(e)
            pass
