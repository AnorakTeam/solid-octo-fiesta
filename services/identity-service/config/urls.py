import os
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'identity-service'})

urlpatterns = [
    path('api/v1/health', health),
    path('api/v1/', include('apps.accounts.urls')),
]

if settings.DEBUG or os.getenv('SERVE_MEDIA', '1') == '1':
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
