from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return self.user.username

class Notes(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100000)
    


