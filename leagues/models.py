from django.db import models

# Create your models here.


class FantasyTeam(models.Model):
    
class User(models.Model):
    
# Player, as well as their aggregate statistics
class Player(models.Model): 
    player_name = models.CharField(max_length=250, primary_key=True)
    
class GameStat(models.Model):
    player = models.ForeignKey(Player)
    
class Game(models.Model):
    