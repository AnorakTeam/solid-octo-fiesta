from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PlayerProgress, PlayerUpgrade
from .serializers import ProgressSerializer, LeaderboardSerializer, UpgradeSerializer
from .upgrades import UPGRADE_CATALOG, serialize_upgrades
class StateView(generics.RetrieveAPIView):
    serializer_class=ProgressSerializer
    def get_object(self): return PlayerProgress.objects.get(user=self.request.user)

class SyncView(generics.GenericAPIView):
    serializer_class=ProgressSerializer
    def post(self,request):
        progress=PlayerProgress.objects.get(user=request.user); value=int(request.data.get('score',0))
        if value < progress.score: value=progress.score
        progress.score=value; progress.save(update_fields=['score','updated_at']); return Response(self.get_serializer(progress).data)
    
class LeaderboardView(generics.GenericAPIView):
    # El ranking es público: no requiere ni procesa credenciales JWT.
    authentication_classes = []
    permission_classes=[permissions.AllowAny]; serializer_class=LeaderboardSerializer
    def get(self,request):
        rows=PlayerProgress.objects.select_related('user').order_by('-score','user__nickname')[:20]
        return Response([
            {
                'position': i,
                'nickname': row.user.nickname,
                'score': row.score,
                'profile_icon': request.build_absolute_uri(row.user.profile_icon.url)
                if row.user.profile_icon else None,
            }
            for i, row in enumerate(rows, 1)
        ])


class UpgradeStateView(generics.GenericAPIView):
    serializer_class = UpgradeSerializer

    def get(self, request):
        return Response(serialize_upgrades(request.user))


class UpgradePurchaseView(generics.GenericAPIView):
    serializer_class = UpgradeSerializer

    def post(self, request, upgrade_key):
        definition = UPGRADE_CATALOG.get(upgrade_key)
        if definition is None:
            return Response(
                {'detail': 'El upgrade solicitado no existe.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        with transaction.atomic():
            progress = PlayerProgress.objects.select_for_update().get(user=request.user)
            if progress.score < definition['cost']:
                return Response(
                    {'detail': 'No tienes puntos suficientes para este upgrade.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            progress.score -= definition['cost']
            progress.save(update_fields=['score', 'updated_at'])

            upgrade, _ = PlayerUpgrade.objects.select_for_update().get_or_create(
                user=request.user,
                upgrade_type=upgrade_key,
            )
            upgrade.quantity += 1
            upgrade.save(update_fields=['quantity', 'updated_at'])

        return Response({
            'score': progress.score,
            **serialize_upgrades(request.user),
        })
