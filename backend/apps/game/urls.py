from django.urls import path
from .views import LeaderboardView, StateView, SyncView, UpgradePurchaseView, UpgradeStateView
urlpatterns=[path('game/state',StateView.as_view()),path('game/sync',SyncView.as_view()),path('game/leaderboard',LeaderboardView.as_view()),path('game/upgrades',UpgradeStateView.as_view()),path('game/upgrades/<str:upgrade_key>/purchase',UpgradePurchaseView.as_view())]
