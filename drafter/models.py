from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
class Player(models.Model): 
    name = models.CharField(max_length=20, primary_key=True)
    team = models.ForeignKey(Team)
    
    def __unicode__(self):
        return self.name

    