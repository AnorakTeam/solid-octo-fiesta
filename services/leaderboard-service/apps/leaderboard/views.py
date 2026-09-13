from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import LeaderboardEntry


class LeaderboardView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rows = LeaderboardEntry.objects.order_by('-score', 'nickname')[:20]
        return Response([
            {
                'position': i,
                'nickname': row.nickname,
                'score': row.score,
                'profile_icon': row.profile_icon,
            }
            for i, row in enumerate(rows, 1)
        ])


class InternalSyncPlayerView(generics.GenericAPIView):
    """Endpoint interno para sincronización directa de jugador si se requiere."""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        nickname = request.data.get('nickname')
        score = request.data.get('score')
        profile_icon = request.data.get('profile_icon')

        if not user_id or not nickname:
            return Response({'detail': 'user_id y nickname son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        entry, created = LeaderboardEntry.objects.get_or_create(
            user_id=user_id,
            defaults={'nickname': nickname, 'score': score or 0, 'profile_icon': profile_icon}
        )

        if not created:
            if nickname:
                entry.nickname = nickname
            if score is not None and int(score) > entry.score:
                entry.score = int(score)
            if profile_icon is not None:
                entry.profile_icon = profile_icon
            entry.save()

        return Response({'status': 'ok', 'user_id': user_id, 'score': entry.score})
