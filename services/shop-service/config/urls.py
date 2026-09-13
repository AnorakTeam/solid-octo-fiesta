from django.http import JsonResponse
from django.urls import include, path

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'shop-service'})

urlpatterns = [
    path('api/v1/health', health),
    path('api/v1/game/upgrades', include('apps.shop.urls')),
]
