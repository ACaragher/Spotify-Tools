<div align="center">


  <h1 align="center">Spotify Tools</h1>

  <p align="center">
    A website to interact with and modify a user's Spotify playlists
  </p>
  <p>
    The website can be accessed at <a href="www.caragher.ie">www.caragher.ie</a>
  </p>
</div>

## About The Project

Website built using Django that provides various tools to create and modify playlists on Spotify. Allows a user to log into the site using their Spotify account letting them use the tools on their own account playlists.

Makes use of the <a href="https://spotipy.readthedocs.io/en/2.22.1/#">Spotipy</a> library and <a href="https://developer.spotify.com/documentation/web-api">Spotify API</a>.

Tools currently implemented are:
* 'Tracks to Playlists' - Pick a playlist and go through it track-by-track, choosing another playlist to add the track to 
* 'Combine Playlists' -  Combine multiple playlists, either into an existing playlist or into a new one 
* 'Genre to Playlist' - Create a new playlist containing every song of a chosen genre from your selected playlists
* 'Shared to Playlist' - Create a new playlist containing the songs that are common to each of your selected playlists


<b>Note that these tools only work with Spotify accounts that have a current premium membership</b>

## Getting Started

To get a local copy up and running follow these steps:

1. Create a Spotify app <a href="https://developer.spotify.com/documentation/web-api/concepts/apps">here</a>. Fill in whatever you wish in each field.
2. Copy the Client ID and Client Secret to `cred.py` in `./spotify_tools`.
Make sure the Redirect URI in your Spotify app matches the Redirect URI in `cred.py`.

3. Install packages in requirements.txt:
   ```sh
   $ pip install -r requirements.txt
   ```
4. Set up database:
   ```sh
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```
5. Run the Django server:
   ```sh
   $ python manage.py runserver
   ```
## Website Screenshots
![Home Page](/Screenshots/Home.PNG)

![Selecting a playlist](/Screenshots/SelectionExample.PNG)

![Track to Playlists](/Screenshots/TrackstoPlaylists.PNG)

![Track to Playlists](/Screenshots/GenretoPlaylist.PNG)
