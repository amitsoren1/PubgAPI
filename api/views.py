from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework import status
from django.conf.urls import url


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
        url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
        response = requests.get(url, headers=HEADER)
        response = json.loads(response.text)
        #print(response["data"]["attributes"]["createdAt"])
        new_match["id"] = response["data"]["id"]
        new_match["begin_at"] = response["data"]["attributes"]["createdAt"]
        new_match["detailed_stats"] = response["data"]["attributes"]["stats"]
        #print(new_match)
        return new_match

    def get_matches(self,tournament_id):
        url = f"https://api.pubg.com/tournaments/{tournament_id}"
        response = requests.get(url, headers=HEADER)
        response = json.loads(response.text)
        matches = []
        for resp in response["data"]["relationships"]["matches"]["data"]:
            match = self.get_match(resp["id"])
            matches.append(match.copy())
        return matches

    def get(self,request):
        url = f"https://api.pubg.com/tournaments"
        response = requests.get(url, headers=HEADER)
        if response.status_code == 404:
            response = json.loads(response.text)
            return Response(response,status.HTTP_404_NOT_FOUND)
        response = json.loads(response.text)
        resp = []
        i=0
        for tournament in response["data"]:
            new_tour = self.tour
            new_tour["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["serie"]["begin_at"] = tournament["attributes"]["createdAt"]
            new_tour["id"] = tournament["id"]
            new_tour["matches"] = self.get_matches(tournament["id"])
            resp.append(new_tour)
            i+=1
            if i ==2:
              break
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
    local_tournament = {
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
    }
    local_tournament["begin_at"] = tournament["begin_at"]
    local_tournament["end_at"] = tournament["end_at"]
    local_tournament["id"] = tournament["id"]
    local_tournament["league_id"] = tournament["league_id"]
    local_tournament["live_supported"] = tournament["live_supported"]
    local_tournament["modified_at"] = tournament["modified_at"]
    local_tournament["name"] = tournament["name"]
    local_tournament["prizepool"] = tournament["prizepool"]
    local_tournament["serie_id"] = tournament["serie_id"]
    local_tournament["slug"] = tournament["slug"]
    local_tournament["winner_id"] = tournament["winner_id"]
    local_tournament["winner_type"] = tournament["winner_type"]
    return local_tournament.copy()

  def get(self,request):
    url = "http://127.0.0.1:8000/tournaments"
    response = requests.get(url)
    response = json.loads(response.text)
    matches = []
    for tournament in response:
      for local_match in tournament["matches"]:
        new_match = self.match.copy()
        new_match["begin_at"] = local_match["begin_at"]
        new_match["detailed_stats"] = local_match["detailed_stats"]
        new_match["id"] = local_match["id"]
        new_match["league"] = tournament["league"]
        new_match["league_id"] = tournament["league_id"]
        new_match["live"] = local_match["live"]
        new_match["live_embed_url"] = local_match["live_embed_url"]
        new_match["live_url"] = local_match["live_url"]
        new_match["match_type"] = local_match["match_type"]
        new_match["modified_at"] = local_match["modified_at"]
        new_match["name"] = local_match["name"]
        new_match["number_of_games"] = local_match["number_of_games"]
        new_match["official_stream_url"] = local_match["official_stream_url"]
        new_match["original_scheduled_at"] = local_match["original_scheduled_at"]
        new_match["rescheduled"] = local_match["rescheduled"]
        new_match["scheduled_at"] = local_match["scheduled_at"]
        new_match["serie"] = tournament["serie"]
        new_match["serie_id"] = tournament["serie_id"]
        new_match["slug"] = local_match["slug"]
        new_match["status"] = local_match["status"]
        new_match["streams"] = local_match["streams"]
        new_match["tournament"] = self.get_tournament(tournament)
        new_match["tournament_id"] = local_match["tournament_id"]
        new_match["winner_id"] = local_match["winner_id"]
        matches.append(new_match.copy())
    return Response(matches)