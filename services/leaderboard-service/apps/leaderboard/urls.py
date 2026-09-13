from django.urls import path
from .views import LeaderboardView, InternalSyncPlayerView

urlpatterns = [
    path('', LeaderboardView.as_view()),
    path('/sync', InternalSyncPlayerView.as_view()),
]
