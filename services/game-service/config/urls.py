from django.http import JsonResponse
from django.urls import include, path

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'game-service'})

urlpatterns = [
    path('api/v1/health', health),
    path('api/v1/game/', include('apps.game.urls')),
    path('api/v1/internal/', include('apps.game.internal_urls')),
]
