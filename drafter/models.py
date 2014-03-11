from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from explorer.models import RawGameData

# Models
"""
Models for real players
"""
class Team(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    
    def __unicode__(self):
        return self.name
    
class Player(models.Model): 
    name = models.CharField(max_length=32, primary_key=True)
    team = models.ForeignKey(Team)
    REGIONS = (('NA', 'North America'),
               ('EU', 'Europe'),)
    region = models.CharField(max_length = 2, choices=REGIONS)
    
    def __unicode__(self):
        return self.name

class User(AbstractUser):
    def may_enter_draft(self, league):
        return league in self.leagues.all() or league.commish == self
    
    class Meta:
        unique_together = (('username', 'email'), )

class League(models.Model):
    name = models.CharField(max_length=64, blank=False)
    public = models.BooleanField(default=False)
    size = models.PositiveIntegerField(default = 8, validators=[MinValueValidator(2), MaxValueValidator(32)])
    draft_start = models.DateTimeField(blank=True, default=lambda: datetime.now()+timedelta(days=30))
    SEASONS = (('S4Sum', 'Season 4 Summer'),
               ('S4Spr', 'Season 4 Spring'),)
    season = models.CharField(max_length = 5, choices=SEASONS, default='S4Spr')
    REGIONS = (('NA', 'North America'),
               ('EU', 'Europe'),
               ('NAEU', 'North America & Europe'),)
    region = models.CharField(max_length = 4, choices=REGIONS, default='NA')
    transactions_per_time_period = models.PositiveIntegerField(default=3)
    TIME_PERIODS = (('D', 'Daily'),
                    ('W', 'Weekly'))
    transaction_time_period = models.CharField(max_length=1, choices=TIME_PERIODS, default='W')
    
    team_size = models.PositiveIntegerField(default=7, validators=[MinValueValidator(5)])
    
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
    players = models.ManyToManyField(Player, related_name='fantasy_teams', through='FantasyContract', blank=True)
    
    class Meta:
        unique_together = (('manager', 'league'), )
        
    def __unicode__(self):
        return self.name + ", " + self.manager.username
    
class Message(models.Model):
    invite = models.BooleanField(default=False)
    request = models.BooleanField(default=False)
    sender = models.ForeignKey(User, related_name="sent_messages")
    recipient = models.ForeignKey(User, related_name="received_messages")
    target_league = models.ForeignKey(League, null=True, blank=True)
    message = models.CharField(max_length = 256, blank=True)
    new = models.BooleanField(default=True)
    
"""
Model for a FantasyTeam's ownership of a player
"""
class FantasyContract(models.Model):
    round = models.PositiveIntegerField(null=True, blank=True)
    pick = models.PositiveIntegerField(null=True, blank=True)
    team = models.ForeignKey(FantasyTeam)
    player = models.ForeignKey(Player)
    
    POSITIONS = (('Top', 'Top'),
                ('Jun', 'Jungle'),
                ('Mid', 'Mid'),
                ('Adc', 'ADC'),
                ('Sup', 'Support'),
                ('Sub', 'Sub'))
    position = models.CharField(max_length=3, choices=POSITIONS)
    
"""
Model for FantasyTeam's matches between each other
"""
class FantasyMatch(models.Model):
    teams = models.ManyToManyField(FantasyTeam)
    date = models.DateTimeField()
    games = models.ManyToManyField(RawGameData, null=True, blank=True)
    
    def clean(self):
        if self.teams.count() > 2:
            raise ValidationError('A FantasyMatch may not have more than two teams')
        if self.teams.count() == 2 and self.teams[0].league != self.teams[1].league:
            raise ValidationError('Both FantasyTeam\'s must be in the same league')
            