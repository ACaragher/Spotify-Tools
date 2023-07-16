from django.shortcuts import render

# Create your views here.
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
        user_playlists = sp.current_user_playlists()['items']
        playlists = []
        for i in range(len(user_playlists)):
            playlists.append(user_playlists[i]['name'])
        return render(request, 'genre_to_playlist/start.html', {'playlists': playlists, 'premium': True})
    else:
        return render(request, 'genre_to_playlist/start.html', {'premium': False})

@login_required
def run(request):
    sp = spotipy.Spotify(auth=Token.objects.filter(user=request.user).first())
    user_playlists = sp.current_user_playlists()['items']
    if request.method == 'POST':
        playlist_checkbox = request.POST.getlist('playlist_checkbox')
        if playlist_checkbox != "":
            playlists = []
            for playlist in playlist_checkbox:
                if playlist == 'liked':
                    playlists.append('liked')
                else:
                    playlists.append(user_playlists[int(playlist)]['id'])
            artist_tracks = get_artist_uris(sp, playlists)
            artist_ids = list(artist_tracks.keys())
            genre_tracks = {}
            for i in range(0, len(artist_ids), 50):
                j = i + 50 if i + 50 < len(artist_ids) else len(artist_ids)
                artists_data = sp.artists(artist_ids[i:j])
                for artist in artists_data["artists"]:
                    for genre in artist['genres']:
                        genre_tracks.setdefault(genre.title(),[]).extend(artist_tracks[artist['uri']])

            request.session["genre_tracks"] = genre_tracks
            request.session.save()
            genre_list = sorted(genre_tracks.keys())
            print(genre_tracks)
            return render(request, 'genre_to_playlist/run.html', {"premium": True, "genres": genre_list})
        
        else:
            playlists = []
            for i in range(len(user_playlists)):
                playlists.append(user_playlists[i]['name'])
            error_text = "Please select which playlist(s) you want to include:"
        return render(request, 'genre_to_playlist/start.html', {"premium": True, "error": True, "error_text": error_text, "playlists": playlists})
    
    return render(request, 'genre_to_playlist/start.html', {'premium': True})

@login_required
def complete(request):
    sp = spotipy.Spotify(auth=Token.objects.filter(user=request.user).first())
    user_playlists = sp.current_user_playlists()['items']
    if request.method == 'POST':
        genre_tracks = request.session['genre_tracks']
        
        tracks_to_add = genre_tracks[request.POST.get('genre_select')]
        new_playlist = sp.user_playlist_create(user=request.user, name=request.POST.get('new_playlist'))['id']
        for i in range(0, len(tracks_to_add), 50):
            j = i + 50 if i + 50 < len(tracks_to_add) else len(tracks_to_add)
            sp.playlist_add_items(playlist_id=new_playlist, items=tracks_to_add[i:j])
        return render(request, 'genre_to_playlist/complete.html')
        
    else:
        playlists = []
        for i in range(len(user_playlists)):
            playlists.append(user_playlists[i]['name'])
        error_text = "Unknown Error"
    return render(request, 'genre_to_playlist/start.html', {"premium": True, "error": True, "error_text": error_text, "playlists": playlists})
    

def get_artist_uris(sp, playlist_ids):
    offset = 0
    artists = {}
    for playlist_id in playlist_ids:
        if playlist_id == 'liked':
            curr_iter_songs= sp.current_user_saved_tracks(offset=offset, limit=LIMIT)['items']
        else:
            curr_iter_songs = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=0)['items']
        
        while curr_iter_songs:
            tracks = [track['track'] for track in curr_iter_songs]
            #artists.update([artist['uri'] for track in tracks for artist in track])
            for track in tracks:
                for artist in track['artists']:
                    artists.setdefault(artist['uri'],[]).append(track['uri'])
            if playlist_id == 'liked':
                offset += 50
                curr_iter_songs = sp.current_user_saved_tracks(offset=offset, limit=LIMIT)['items']
            else:
                offset += 100
                curr_iter_songs = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=offset)['items']

    return artists