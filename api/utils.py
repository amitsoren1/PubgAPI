import requests
import json
from api.models import Tournament,Match

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
            tournament_ids.append(tournament.id)
        for tournament in response["data"]:
            if tournament["id"] not in tournament_ids:
                obj = Tournament.objects.create(tournament_id=tournament["id"],
                                                tournament=json.dumps(tournament))
                obj.save()
    
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
            print(u'\u2713')
                
