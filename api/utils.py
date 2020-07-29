import requests
import json
from api.models import Tournament,Match,Player

HEADER = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhZGVhMzQwMC1hZDhhLTAxMzgtM2IyMS0xYmJkOWE0ZjQyNzEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTk1MzQwOTgzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Imx1Y2lmZXJoZWxsNjA2In0.NwsthIsl-D6uuiI0a7zwwk6gJrY1MeYwUudtCJYRXJc",
  "Accept": "application/vnd.api+json"
}

class UpdateData():
    def update_tournaments(self):
        url = "https://api.pubg.com/tournaments"
        response = requests.get(url,headers=HEADER)
        response = json.loads(response.text)
        tournaments = Tournament.objects.all()
        tournament_ids = []
        for tournament in tournaments:
            tournament_ids.append(tournament.tournament_id)
        for tournament in response["data"]:
            if tournament["id"] not in tournament_ids:
                obj = Tournament.objects.create(tournament_id=tournament["id"],
                                                tournament=json.dumps(tournament))
                obj.save()
            print(tournament["id"], u'\u2713')
    
    def update_match(self,match_id,tournament_id):
        if Match.objects.filter(match_id=match_id).count()==0:
            url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
            response = requests.get(url, headers=HEADER)
            response = json.loads(response.text)
            obj = Match.objects.create(match_id=response["data"]["id"],
                                        match=json.dumps(response),
                                        tour_id=tournament_id)
            obj.save()


    '''def get_matches(self,tournament_id):
        url = f"https://api.pubg.com/tournaments/{tournament_id}"
        response = requests.get(url, headers=HEADER)
        response = json.loads(response.text)
        matches = []
        for resp in response["data"]["relationships"]["matches"]["data"]:
            match = self.get_match(resp["id"])
            matches.append(match.copy())
        return matches'''

    def update_matches(self):
        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            url = f"https://api.pubg.com/tournaments/{tournament.tournament_id}"
            response = requests.get(url, headers=HEADER)
            if response is None:
                continue
            response = json.loads(response.text)
            for resp in response["data"]["relationships"]["matches"]["data"]:
                self.update_match(resp["id"],tournament.tournament_id)
            print(resp["id"], u'\u2713')

    def update_players(self):
        matches = Match.objects.all()
        players = Player.objects.all()
        player_ids = [player.player_id for player in players]
        for match in matches:
            match = json.loads(match.match)
            for participant in match["included"]:
                if participant["type"] == "participant" and participant["attributes"]["shardId"] == "steam":
                    account_id = participant["attributes"]["stats"]["playerId"]
                    if account_id not in player_ids:
                        url = f"https://api.pubg.com/shards/steam/players/{account_id}"
                        try:
                            response = requests.get(url, headers=HEADER)
                            response = json.loads(response.text)
                        except:
                            continue
                        obj = Player.objects.create(player_id=account_id,player=json.dumps(response))
                        obj.save()
                        print(account_id, u'\u2713')
                    else:
                        try:
                            existing_player = Player.objects.filter(player_id=account_id).first()
                            existing_player_matches = []
                            existing_player_details = json.loads(existing_player.player)
                            for local_match in existing_player_details["data"][0]["relationships"]["matches"]["data"]:
                                existing_player_matches.append(local_match.id)
                            if match["data"]["id"] not in existing_player_matches:
                                existing_player.delete()
                                url = f"https://api.pubg.com/shards/steam/players/{account_id}"
                                try:
                                    response = requests.get(url, headers=HEADER)
                                except:
                                    continue
                                obj = Player.objects.create(player_id=account_id,player=response)
                                obj.save()
                                print(account_id, u'\u2713')
                        except:
                            pass