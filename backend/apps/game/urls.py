from django.urls import path
from .views import StateView,SyncView,LeaderboardView
urlpatterns=[path('game/state',StateView.as_view()),path('game/sync',SyncView.as_view()),path('game/leaderboard',LeaderboardView.as_view())]
