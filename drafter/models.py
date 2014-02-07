from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Models

class User(AbstractUser):
    def in_league(self, league):
        return league in self.teams.all()
    
    def is_commish(self, league):
        return league in self.managed_leagues.all()
    
    def is_draftable(self, league):
        return self.in_league(league) or self.is_commish(league)
    
    class Meta:
        unique_together = (('username', 'email'), )

class League(models.Model):
    name = models.CharField(max_length=64, blank=False)
    public = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    size = models.PositiveIntegerField(default = 12, validators=[MinValueValidator(2), MaxValueValidator(32)])
    
    commish = models.ForeignKey(User, related_name='managed_leagues')
    teams = models.ManyToManyField(User, related_name='teams', blank=True, through='FantasyTeam')
    
    def __unicode__(self):
        return self.name

class FantasyTeam(models.Model):
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    name = models.CharField(max_length=32, default="The Bedazzling Defaults")
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    draft_pick = models.PositiveIntegerField(null=True)
    
    class Meta:
        unique_together = (('manager', 'league'), )
        
    def __unicode__(self):
        return self.name


"""
Models for real players
"""
class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    
    def __unicode__(self):
        return self.name
    
class Player(models.Model): 
    name = models.CharField(max_length=20, primary_key=True)
    team = models.ForeignKey(Team)
    
    def __unicode__(self):
        return self.name
