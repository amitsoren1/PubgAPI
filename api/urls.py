from .views import ListUsers,ListMatches
from django.urls import path

app_name = "api"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('user/<str:user_id>', ListUsers.as_view()),
    path('match/<str:match_id>',ListMatches.as_view())
]