from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework import status
from django.conf import settings
from django.conf.urls import url
from django.urls import reverse
from api.models import Tournament,Match

HEADER = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhZGVhMzQwMC1hZDhhLTAxMzgtM2IyMS0xYmJkOWE0ZjQyNzEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTk1MzQwOTgzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Imx1Y2lmZXJoZWxsNjA2In0.NwsthIsl-D6uuiI0a7zwwk6gJrY1MeYwUudtCJYRXJc",
  "Accept": "application/vnd.api+json"
}

platform = ["console","kakao","psn","stadia","steam","tournament","xbox"]

class ListUsers(APIView):
    def get(self, request,user_id=None):
        url = f"https://api.pubg.com/shards/steam/players/{user_id}"
        response = requests.get(url, headers=HEADER)
        if response.status_code == 404:
            response = json.loads(response.text)
            return Response(response,status.HTTP_404_NOT_FOUND)
        response = json.loads(response.text)
        resp = {
            "birth_year": None,
            "birthday": None,
            "current_team": None,
            "current_videogame": None,
            "first_name": None,
            "hometown": None,
            "id": None,
            "image_url": None,
            "last_name": None,
            "name": None,
            "nationality": None,
            "role": None,
            "slug": None
        }

        resp['id'] = response['data']['id']
        resp['name'] = response['data']['attributes']['name']
        return Response(resp)

class ListMatch(APIView):
    def get(self, request,match_id=None):
        url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
        response = requests.get(url, headers=HEADER)
        if response.status_code == 404:
            response = json.loads(response.text)
            return Response(response,status.HTTP_404_NOT_FOUND)
        response = json.loads(response.text)
        resp = {
            "begin_at": None,
            "detailed_stats": None,
            "draw": None,
            "end_at": None,
            "forfeit": None,
            "game_advantage": None,
            "games": [],
            "id": None,
            "league": {},
            "league_id": None,
            "live": {},
            "live_embed_url": None,
            "live_url": None,
            "match_type": None,
            "modified_at": None,
            "name": None,
            "number_of_games": None,
            "official_stream_url": None,
            "opponents": [],
            "original_scheduled_at": None,
            "rescheduled": None,
            "results": [],
            "scheduled_at": None,
            "serie": {},
            "serie_id": None,
            "slug": None,
            "status": None,
            "streams": {},
            "tournament": {},
            "tournament_id": None,
            "videogame": {},
            "videogame_version": None,
            "winner": {},
            "winner_id": None
            }
        resp['id'] = response['data']['id']
        resp['status'] = response['data']['attributes']['seasonState']
        return Response(resp)

class ListTournaments(APIView):
    team = {
        "acronym": None,
        "id": None,
        "image_url": None,
        "location": None,
        "modified_at": None,
        "name": None,
        "slug": None
      }
    match = {
        "begin_at": None,
        "detailed_stats": None,
        "draw": None,
        "end_at": None,
        "forfeit": None,
        "game_advantage": None,
        "id": None,
        "live": {
          "opens_at": None,
          "supported": None,
          "url": None
                },
        "live_embed_url": None,
        "live_url": None,
        "match_type": None,
        "modified_at": None,
        "name": None,
        "number_of_games": None,
        "official_stream_url": None,
        "original_scheduled_at": None,
        "rescheduled": None,
        "scheduled_at": None,
        "slug": None,
        "status": None,
        "streams": {
          "english": {
            "embed_url": None,
            "raw_url": None
          },
          "russian": {
            "embed_url": None,
            "raw_url": None
          }
        },
        "tournament_id": None,
        "winner_id": None
      }

    tour =   {
    "begin_at": None,
    "end_at": None,
    "id": None,
    "league": {
      "id": None,
      "image_url": None,
      "modified_at": None,
      "name": None,
      "slug": None,
      "url": "https://www.pubg.com/"
                },
    "league_id": None,
    "live_supported": None,
    "matches": [],
    "modified_at": None,
    "name": None,
    "prizepool": None,
    "serie": {
      "begin_at": None,
      "description": None,
      "end_at": None,
      "full_name": None,
      "id": None,
      "league_id": None,
      "modified_at": None,
      "name": None,
      "season": None,
      "slug": None,
      "tier": None,
      "winner_id": None,
      "winner_type": None,
      "year": None
    },
    "serie_id": None,
    "slug": None,
    "teams": [],
    "videogame": {
      "id": None,
      "name": "PUBG",
      "slug": "pubg"
    },
    "winner_id": None,
    "winner_type": None
  }
    '''def get_tournament(self,tournament_id):
        new_tour = self.tour
        url = f"https://api.pubg.com/shards/tournaments/{tournament_id}"
        response = requests.get(url, headers=HEADER)
        response = json.loads(response.text)
        for match in response["data"]["relationships"]["matches"]["data"]:
            '''
    def get_match(self,match_id):
        new_match = self.match
        #url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
        response = Match.objects.filter(match_id=match_id).first()
        response = json.loads(response.match)
        #print(response["data"]["attributes"]["createdAt"])
        new_match["id"] = response["data"]["id"]
        new_match["begin_at"] = response["data"]["attributes"]["createdAt"]
        new_match["detailed_stats"] = response["data"]["attributes"]["stats"]
        #print(new_match)
        return new_match

    def get_matches(self,tournament_id):
        #url = f"https://api.pubg.com/tournaments/{tournament_id}"
        response = Match.objects.all().filter(tour_id=tournament_id)
        matches = []
        for resp in response:
            match = self.get_match(resp.match_id)
            matches.append(match.copy())
        return matches

    def get(self,request):
        resp = []
        i=0
        tournaments = Tournament.objects.all()
        for obj in tournaments:
            tournament = json.loads(obj.tournament)
            new_tour = self.tour
            new_tour["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["serie"]["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["id"] = tournament["id"]
            new_tour["matches"] = self.get_matches(tournament["id"])
            resp.append(new_tour.copy())
            i+=1
            '''if i ==2:
              break'''
        return Response(resp)

class ListMatches(APIView):
  match = {
    "begin_at": None,
    "detailed_stats": None,
    "draw": None,
    "end_at": None,
    "forfeit": None,
    "game_advantage": None,
    "games": [
      {
        "begin_at": None,
        "detailed_stats": None,
        "end_at": None,
        "finished": None,
        "forfeit": None,
        "id": None,
        "length": None,
        "match_id": None,
        "position": None,
        "status": None,
        "video_url": None,
        "winner": {
          "id": None,
          "type": None
        },
        "winner_type": None
      }
    ],
    "id": None,
    "league": {
      "id": None,
      "image_url": None,
      "modified_at": None,
      "name": None,
      "slug": None,
      "url": "https://www.pubg.com/"
    },
    "league_id": None,
    "live": {
      "opens_at": None,
      "supported": None,
      "url": None
    },
    "live_embed_url": None,
    "live_url": None,
    "match_type": None,
    "modified_at": None,
    "name": None,
    "number_of_games": None,
    "official_stream_url": None,
    "opponents": [
      {
        "opponent": {
          "acronym": None,
          "id": None,
          "image_url": None,
          "location": None,
          "modified_at": None,
          "name": None,
          "slug": None
        },
        "type": None
      },
    ],
    "original_scheduled_at": None,
    "rescheduled": None,
    "results": [
      {
        "score": None,
        "team_id": None
      }
    ],
    "scheduled_at": None,
    "serie": {
      "begin_at": None,
      "description": None,
      "end_at": None,
      "full_name": None,
      "id": None,
      "league_id": None,
      "modified_at": None,
      "name": None,
      "season": None,
      "slug": None,
      "tier": None,
      "winner_id": None,
      "winner_type": None,
      "year": None
    },
    "serie_id": None,
    "slug": None,
    "status": None,
    "streams": {
      "english": {
        "embed_url": None,
        "raw_url": None
      },
      "russian": {
        "embed_url": None,
        "raw_url": None
      }
    },
    "tournament": {
      "begin_at": None,
      "end_at": None,
      "id": None,
      "league_id": None,
      "live_supported": None,
      "modified_at": None,
      "name": None,
      "prizepool": None,
      "serie_id": None,
      "slug": None,
      "winner_id": None,
      "winner_type": None
    },
    "tournament_id": None,
    "videogame": {
      "id": None,
      "name": "PUBG",
      "slug": "pubg"
    },
    "videogame_version": None,
    "winner": {
      "acronym": None,
      "id": None,
      "image_url": None,
      "location": None,
      "modified_at": None,
      "name": None,
      "slug": None
    },
    "winner_id": None
  }
  def get_tournament(self,tournament):
    local_tournament = {}
    attrs = [
      "begin_at",
      "end_at",
      "id",
      "league_id",
      "live_supported",
      "modified_at",
      "name",
      "prizepool",
      "serie_id",
      "slug",
      "winner_id",
      "winner_type"
      ]
    for attr in attrs:
      local_tournament[attr] = tournament[attr]
    return local_tournament.copy()

  def get(self,request):
    url = "http://"+f"{settings.ALLOWED_HOSTS[0]}"+":8000/tournaments"
    response = requests.get(url)
    response = json.loads(response.text)
    matches = []
    match_attributes = [
      "begin_at",
      "detailed_stats",
      "id",
      "live",
      "live_embed_url",
      "live_url",
      "match_type",
      "modified_at",
      "name",
      "number_of_games",
      "official_stream_url",
      "original_scheduled_at",
      "rescheduled",
      "scheduled_at",
      "slug",
      "status",
      "streams",
      "tournament_id",
      "winner_id",
    ]
    tournament_attributes = [
      "league",
      "league_id",
      "serie",
      "serie_id",
      "tournament",
    ]
    for tournament in response:
      for local_match in tournament["matches"]:
        new_match = self.match.copy()
        for attr in match_attributes:
          new_match[attr] = local_match[attr]
        for attr in tournament_attributes:
          if attr!="tournament":
            new_match[attr] = tournament[attr]
          else:
            new_match[attr] = self.get_tournament(tournament)
        matches.append(new_match.copy())
    return Response(matches)