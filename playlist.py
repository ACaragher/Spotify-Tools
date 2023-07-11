import PySimpleGUI as sg

def liked_to_playlists(sp, web_device):
    # Get all of the user's playlists
    user = sp.current_user()
    playlists = sp.user_playlists(user['id'])['items']

    next = " "
    curr_offset = 0
    
    # Loop through all of the user's liked songs
    while next:
        # Get next 50 tracks (50 is the max number of tracks that can be retreived per call)
        liked_songs = sp.current_user_saved_tracks(offset=curr_offset, limit=50)
        next = liked_songs['next']
        for i in range(len(liked_songs)):
                valid = False

                track = liked_songs['items'][i]['track']
                artist = track['artists'][0]['name']
                sp.start_playback(web_device, uris=[track['uri']],position_ms=0)

                # Create GUI displaying the name of each playlist as a button
                buttons = [[sg.Button(playlist['name'], size=(15,2)),] for playlist in playlists]
                layout = [[sg.Text(f"Track - '{track['name']}'\nArtist - '{artist}'\n")]] + buttons
                window = sg.Window("Playlists", layout, element_justification='c', default_element_size=(15,1))
                event, values = window.read()
                # If user closes the window
                if event == sg.WIN_CLOSED:
                    next = False
                    print("Exiting...")
                    sp.pause_playback(web_device)
                    break
                else:
                    # Check which playlist the user has selected and add the current song to that playlist
                    for playlist in playlists:
                         if playlist['name'] == event:
                            sp.playlist_add_items(playlist_id=playlist['id'], items=[track['uri']])
                    window.close()
                
        curr_offset += 50
