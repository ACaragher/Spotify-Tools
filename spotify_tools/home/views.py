from django.shortcuts import render
from django.shortcuts import redirect
from . import config
from social_django.models import UserSocialAuth

def index(request):
    return render(request, 'home/index.html')

def spotify_login(request):
    sp_auth = config.sp_auth
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

def spotify_login_complete(request):
    context = {
        'access_token': UserSocialAuth.objects.last().extra_data['access_token']
    }
    return render(request, 'home/index.html', context)
