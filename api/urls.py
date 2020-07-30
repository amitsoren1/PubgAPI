from api.views import List1User,List1Match,ListTournaments,ListMatches,ListPlayers
from django.urls import path

app_name = "api"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('user/<str:user_id>', List1User.as_view()),
    path('match/<str:match_id>',List1Match.as_view()),
    path('tournaments/',ListTournaments.as_view()),
    path('matches/',ListMatches.as_view()),
    path('players/',ListPlayers.as_view())
]