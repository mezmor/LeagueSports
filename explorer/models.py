from django.db import models

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
    
    # week = models.PositiveIntegerField()
    
    
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
    