from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import PositiveIntegerField

# Models
 
class League(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    
    def __unicode__(self):
        return self.name

class FantasyTeam(models.Model):
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    public = models.BooleanField()
    name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
#    ties = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = (('manager', 'league'), )
        
    def __unicode__(self):
        return (self.manager, self.league)
    
# Player, as well as their aggregate statistics
class Player(models.Model): 
    name = models.CharField(max_length=20, primary_key=True)
    team = models.ForeignKey(Team)
    
    def __unicode__(self):
        return self.name
    
    
class Game(models.Model):
    winner = models.ForeignKey(Team, related_name='games_won')
    date = models.DateTimeField()
    duration = models.TimeField()
    blue_score = PositiveIntegerField(default=0)
    red_score = PositiveIntegerField(default=0)
    
    blue_ban_one = models.CharField(max_length=20)
    blue_ban_two = models.CharField(max_length=20)
    blue_ban_three = models.CharField(max_length=20)
    red_ban_one = models.CharField(max_length=20)
    red_ban_two = models.CharField(max_length=20)
    red_ban_three = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.date
    

class PlayerGameStat(models.Model):
    player = models.ForeignKey(Player, related_name='game_stats')
    game = models.ForeignKey(Game, related_name='player_stats')
    
    COLOR_CHOICES = (
            ('blue', 'blue'),
            ('red', 'red'))
    team_color = models.CharField(choices=COLOR_CHOICES, max_length=5)
    
    kills = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    creeps = models.PositiveIntegerField()
    
    champion = models.CharField(max_length=20)
    summoner_one = models.CharField(max_length=20)
    summoner_two = models.CharField(max_length=20)
    items = models.CharField(max_length=250) # Pipe delimited
    
    class Meta:
        unique_together = (('player', 'game'), )
        
    def __unicode__(self):
        return (self.player, self.game)
        