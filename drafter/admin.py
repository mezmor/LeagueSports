from django.contrib import admin
from drafter.models import *
from django.contrib.sites.models import Site

class LeagueAdmin(admin.ModelAdmin):
    pass

admin.site.register(League, LeagueAdmin)
admin.site.register(Team, LeagueAdmin)
admin.site.register(FantasyTeam, LeagueAdmin)
admin.site.register(Player, LeagueAdmin)
admin.site.register(Game, LeagueAdmin)
admin.site.register(PlayerGameStat, LeagueAdmin)
admin.site.unregister(Site)