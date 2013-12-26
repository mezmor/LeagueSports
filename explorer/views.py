import json
from django.http import HttpResponse
from django.shortcuts import render
from explorer.models import RawPlayerData

def explorer(request):
    return render(request, 'explorer/index.html');

def get_player_names(request):
    if request.method == 'GET':
        all_players = list(RawPlayerData.objects.values_list('player_name', flat=True))
        
        response_data = {}
        response_data['data'] = []
        for name in sorted(set(all_players)):
            if name != "":
                player_data = {}
                player_data['name'] = name
                player_data['sample'] = all_players.count(name)
                response_data['data'].append(player_data)
            
        return HttpResponse(json.dumps(response_data), content_type="application/json")
