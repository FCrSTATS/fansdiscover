from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    # pass
    first_name = models.CharField(max_length = 15, default=' ')
    last_name = models.CharField(max_length = 15, default= ' ')
    avatar_url = models.CharField(max_length = 50, default=' ')

    def __str__(self):
        return self.username
