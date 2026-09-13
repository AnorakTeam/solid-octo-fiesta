from django.http import JsonResponse
from django.urls import include, path

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'leaderboard-service'})

urlpatterns = [
    path('api/v1/health', health),
    path('api/v1/game/leaderboard', include('apps.leaderboard.urls')),
]
