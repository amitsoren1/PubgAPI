from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework import status


header = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhZGVhMzQwMC1hZDhhLTAxMzgtM2IyMS0xYmJkOWE0ZjQyNzEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTk1MzQwOTgzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Imx1Y2lmZXJoZWxsNjA2In0.NwsthIsl-D6uuiI0a7zwwk6gJrY1MeYwUudtCJYRXJc",
  "Accept": "application/vnd.api+json"
}

platform = ["console","kakao","psn","stadia","steam","tournament","xbox"]

class ListUsers(APIView):
    def get(self, request,user_id=None):
        url = f"https://api.pubg.com/shards/steam/players/{user_id}"
        response = requests.get(url, headers=header)
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

class ListMatches(APIView):
    def get(self, request,match_id=None):
        url = f"https://api.pubg.com/shards/steam/matches/{match_id}"
        response = requests.get(url, headers=header)
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
        response = requests.get(url, headers=header)
        response = json.loads(response.text)
        for match in response["data"]["relationships"]["matches"]["data"]:
            '''
    def get_match(self,match_id):
        new_match = self.match
        url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
        response = requests.get(url, headers=header)
        response = json.loads(response.text)
        #print(response["data"]["attributes"]["createdAt"])
        new_match["id"] = response["data"]["id"]
        new_match["begin_at"] = response["data"]["attributes"]["createdAt"]
        new_match["detailed_stats"] = response["data"]["attributes"]["stats"]
        #print(new_match)
        return new_match

    def get_matches(self,tournament_id):
        url = f"https://api.pubg.com/tournaments/{tournament_id}"
        response = requests.get(url, headers=header)
        response = json.loads(response.text)
        matches = []
        for resp in response["data"]["relationships"]["matches"]["data"]:
            match = self.get_match(resp["id"])
            matches.append(match.copy())
        return matches

    def get(self,request):
        url = f"https://api.pubg.com/tournaments"
        response = requests.get(url, headers=header)
        if response.status_code == 404:
            response = json.loads(response.text)
            return Response(response,status.HTTP_404_NOT_FOUND)
        response = json.loads(response.text)
        resp = []
        for tournament in response["data"]:
            new_tour = self.tour
            new_tour["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["serie"]["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["id"] = tournament["id"]
            new_tour["matches"] = self.get_matches(tournament["id"])
            resp.append(new_tour)
        return Response(resp)