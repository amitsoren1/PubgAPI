from .views import ListUsers,ListMatches,ListTournaments,ListMatch
from django.urls import path

app_name = "api"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('user/<str:user_id>', ListUsers.as_view()),
    path('match/<str:match_id>',ListMatch.as_view()),
    path('tournaments/',ListTournaments.as_view()),
    path('matches/',ListMatches.as_view()),
]