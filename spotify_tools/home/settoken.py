from .models import Token

def set_token(backend, response, details, user, *args, **kwargs):
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    auth_time = response['expires_in']
    token_type = response['token_type']
    """"
    if Token.objects.filter(user=user).exists():
        token = Token.objects.filter(user=user)..update_token(access_token, refresh_token, auth_time, token_type)
        token.save()
    else:
        token = Token(user=user, access_token=access_token, refresh_token=refresh_token, auth_time=auth_time, token_type=token_type)
        token.save()

    """
    token, created = Token.objects.update_or_create(user=user, defaults={'access_token': access_token, 'refresh_token': refresh_token,
                                                                          'auth_time': auth_time, 'token_type': token_type})
    token.save()
    
    def __str__():
        return f"Username: {user.username}, Access_Token: {access_token}" 