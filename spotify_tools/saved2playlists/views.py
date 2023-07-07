from django.shortcuts import render

def begin(request):
    return render(request, 'saved2playlists/begin.html')

