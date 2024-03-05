from django.shortcuts import render
from spotify_tools import config

def start(request):
    sp = config.get_user_auth(request.user)
 
    if sp.current_user()['product'] == 'premium':
        user_playlists = sp.current_user_playlists()['items']
        playlists = []
        for i in range(len(user_playlists)):
            playlists.append(user_playlists[i]['name'])
        return render(request, 'combine_playlists/start.html', {'playlists': playlists, 'premium': True})
    return render(request, 'combine_playlists/start.html', {'premium': False})