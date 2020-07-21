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