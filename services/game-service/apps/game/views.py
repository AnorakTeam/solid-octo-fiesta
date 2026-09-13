from django.conf import settings
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PlayerProgress
from .serializers import ProgressSerializer
from .events import publish_event


class StateView(generics.GenericAPIView):
    serializer_class = ProgressSerializer

    def get(self, request):
        progress, _ = PlayerProgress.objects.get_or_create(user_id=request.user.id)
        return Response(self.get_serializer(progress).data)


class SyncView(generics.GenericAPIView):
    serializer_class = ProgressSerializer

    def post(self, request):
        progress, _ = PlayerProgress.objects.get_or_create(user_id=request.user.id)
        value = int(request.data.get('score', 0))
        if value < progress.score:
            value = progress.score

        if value != progress.score or progress.created_at == progress.updated_at:
            progress.score = value
            progress.save(update_fields=['score', 'updated_at'])
            # Emitir evento al bus para alimentar la proyección del ranking
            publish_event('game_events', {
                'event': 'score_updated',
                'user_id': request.user.id,
                'nickname': request.user.nickname,
                'score': progress.score,
            })

        return Response(self.get_serializer(progress).data)


class InternalDeductPointsView(generics.GenericAPIView):
    """Endpoint interno protegido para que shop-service descuente saldo de forma atómica."""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        secret = request.headers.get('X-Internal-Secret')
        if secret != getattr(settings, 'INTERNAL_API_SECRET', None):
            return Response({'detail': 'No autorizado.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        cost = int(request.data.get('cost', 0))

        if not user_id or cost < 0:
            return Response({'detail': 'Parámetros inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            progress, _ = PlayerProgress.objects.select_for_update().get_or_create(user_id=user_id)
            if progress.score < cost:
                return Response(
                    {'detail': 'No tienes puntos suficientes para este upgrade.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            progress.score -= cost
            progress.save(update_fields=['score', 'updated_at'])

            publish_event('game_events', {
                'event': 'score_updated',
                'user_id': user_id,
                'nickname': request.data.get('nickname', f"player_{user_id}"),
                'score': progress.score,
            })

        return Response({'score': progress.score})
