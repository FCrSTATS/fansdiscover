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


class Player(models.Model):
    objects = models.Manager()
    pid = models.IntegerField(primary_key=True)
    player = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    age = models.IntegerField()
    value = models.IntegerField()
    nationality = models.CharField(max_length=400)
    avi = models.URLField()

    def __str__(self):
        return self.player

class Report(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rid = models.IntegerField(serialize=True)
    opponent = models.CharField(max_length=200)
    date = models.DateField()
    report = models.TextField(max_length=100000)
    performance_score = models.FloatField()
    potential_score = models.FloatField()
    value_score = models.FloatField()
    
    