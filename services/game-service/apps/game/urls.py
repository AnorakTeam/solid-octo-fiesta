from django.urls import path
from .views import StateView, SyncView

urlpatterns = [
    path('state', StateView.as_view()),
    path('sync', SyncView.as_view()),
]
