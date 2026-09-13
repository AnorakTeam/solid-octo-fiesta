import os
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})

urlpatterns = [
    path('api/v1/health', health), 
    path('api/v1/', include('apps.accounts.urls')), 
    path('api/v1/', include('apps.game.urls'))
]

if settings.DEBUG or os.getenv('SERVE_MEDIA', '1') == '1':
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

