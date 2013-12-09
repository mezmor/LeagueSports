from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import PositiveIntegerField

# Models
 
class League(models.Model):
    name = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.name
    
class User(AbstractUser):
    leagues = models.ManyToManyField(League)

class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    
    def __unicode__(self):
        return self.name

class FantasyTeam(models.Model):
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    public = models.BooleanField(default=True)
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
        

class RawGameData(models.Model):
    # id is auto generated as primary key
    blueTeam = models.CharField(max_length = 10)
    redTeam = models.CharField(max_length = 10)
    blueTeamSeriesScore = models.PositiveIntegerField()
    redTeamSeriesScore = models.PositiveIntegerField()
    blueTeamBan1 = models.CharField(max_length = 20)
    blueTeamBan2 = models.CharField(max_length = 20)
    blueTeamBan3 = models.CharField(max_length = 20)
    redTeamBan1 = models.CharField(max_length = 20)
    redTeamBan2 = models.CharField(max_length = 20)
    redTeamBan3 = models.CharField(max_length = 20)
    date = models.DateTimeField()
    duration = models.TimeField()
    tournament = models.CharField(max_length = 100)
    
    
class RawPlayerData(models.Model):
    game = models.ForeignKey(RawGameData, related_name='player_data')
    player_name = models.CharField(max_length = 20)
    player_name.db_index = True
    team_color = models.CharField(max_length = 10)
    champion = models.CharField(max_length = 50)
    kills = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    cs = models.PositiveIntegerField()
    summonerspells = models.CharField(max_length = 50)
    items = models.CharField(max_length = 500)
    
    class Meta:
        unique_together = (('game', 'player_name'), )
    
    