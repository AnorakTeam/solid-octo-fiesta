from django.urls import path
from .views import UpgradeStateView, UpgradePurchaseView

urlpatterns = [
    path('', UpgradeStateView.as_view()),
    path('/<str:upgrade_key>/purchase', UpgradePurchaseView.as_view()),
]
