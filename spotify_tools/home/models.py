from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=300)

    def __str__(self):
        return self.access_token
    
    def update_token(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.save()

    def refresh_access_token(self, sp_oauth):
        updated_token = sp_oauth.refresh_access_token(refresh_token=self.refresh_token)
        self.update_token(access_token=updated_token['access_token'], refresh_token=updated_token['refresh_token'])
        
