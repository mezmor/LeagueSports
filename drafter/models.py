from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Models

class User(AbstractUser):
    def may_enter_draft(self, league):
        return league in self.leagues.all() or league.commish == self
    
    class Meta:
        unique_together = (('username', 'email'), )

class League(models.Model):
    name = models.CharField(max_length=64, blank=False)
    public = models.BooleanField(default=False)
    size = models.PositiveIntegerField(default = 8, validators=[MinValueValidator(2), MaxValueValidator(32)])
    draft_start = models.DateTimeField(null=True, blank=True)
    SEASONS = (('S4Sum', 'Season 4 Summer'),
               ('S4Spr', 'Season 4 Spring'),)
    season = models.CharField(max_length = 5, choices=SEASONS, default='S4Spr')
    REGIONS = (('NA', 'North America'),
               ('EU', 'Europe'),
               ('NAEU', 'North America & Europe'),               )
    region = models.CharField(max_length = 4, choices=REGIONS, default='NA')
    transactions_per_time = models.PositiveIntegerField(default=3)
    TIME_PERIODS = (('D', 'Daily'),
                    ('W', 'Weekly'))
    transaction_time_period = models.CharField(max_length=1, choices=TIME_PERIODS, default='W')
    
    team_size = models.PositiveIntegerField(default=5, validators=[MinValueValidator(5)])
    
    commish = models.ForeignKey(User, related_name='managed_leagues')
    users = models.ManyToManyField(User, related_name='leagues', blank=True, through='FantasyTeam')
    
    top_score = models.CharField(max_length = 64, default="([kda] * 15 + [cs]) / [game time]")
    jungle_score = models.CharField(max_length = 64, default="([kda] * 25 + [cs]) / [game time]")
    mid_score = models.CharField(max_length = 64, default="([kda] * 15 + [cs]) / [game time]")
    ad_score = models.CharField(max_length = 64, default="([kda] * 15 + [cs]) / [game time]")
    support_score = models.CharField(max_length = 64, default="([kda] + [gold]) * 25 / [game time]")
    
    per_game_losing_mod = models.CharField(max_length = 32, default="[score]*0.8")
    per_game_godly_mod = models.CharField(max_length = 32, default="[score]*1.2")
    
    season_length = models.PositiveIntegerField(default=8)
            
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
    locked = models.BooleanField(default=False)
    
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

"""
Model for draft
"""
class Draft(models.Model):
    league = models.ForeignKey(League)
    round = models.PositiveIntegerField()
    pick = models.PositiveIntegerField()
    team = models.ForeignKey(FantasyTeam)
    player = models.ForeignKey(Player)