from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300)
    auth_time = models.IntegerField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        return self.access_token
    
    def update_token(self, access_token, refresh_token, auth_time, token_type):
        self.access_token = access_token
        self.refresh_token=refresh_token
        self.auth_time = auth_time
        self.token_type = token_type