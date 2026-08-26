from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
@api_view(['GET'])
@permission_classes([AllowAny])
def health(request): return Response({'status':'ok'})
urlpatterns = [path('api/v1/health', health), 
               path('api/v1/', include('apps.accounts.urls')), 
               path('api/v1/', include('apps.game.urls'))
               ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
