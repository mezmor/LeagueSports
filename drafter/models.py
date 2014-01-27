from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Models

class User(AbstractUser):
    class Meta:
        unique_together = (('username', 'email'), )
 
class League(models.Model):
    name = models.CharField(max_length=64, blank=False)
    public = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    size = models.PositiveIntegerField(default = 12, validators=[MinValueValidator(2), MaxValueValidator(32)])
    
    commish = models.ForeignKey(User, related_name='managed_leagues')
    users = models.ManyToManyField(User, related_name='leagues', blank=True)
    
    
    def __unicode__(self):
        return self.name

class FantasyTeam(models.Model):
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = (('manager', 'league'), )
        
    def __unicode__(self):
        return (self.manager, self.league)

class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    
    def __unicode__(self):
        return self.name
    
class Player(models.Model): 
    name = models.CharField(max_length=20, primary_key=True)
    team = models.ForeignKey(Team)
    
    def __unicode__(self):
        return self.name
