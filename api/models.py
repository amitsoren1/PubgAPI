from django.db import models

# Create your models here.
class Tournament(models.Model):
    tournament_id = models.TextField(primary_key=True)
    tournament = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.tournament_id}"

class Match(models.Model):
    match_id = models.TextField(primary_key=True)
    tour_id = models.TextField(blank=True,null=True)
    match = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.match_id}"

class Player(models.Model):
    player_id = models.TextField(primary_key=True)
    player = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.player_id}"