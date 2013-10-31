from django.contrib import admin
from drafter.models import League
from django.contrib.sites.models import Site

class LeagueAdmin(admin.ModelAdmin):
    pass

admin.site.register(League, LeagueAdmin)
admin.site.unregister(Site)