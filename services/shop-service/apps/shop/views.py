import requests
from django.conf import settings
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from .models import PlayerUpgrade
from .upgrades import UPGRADE_CATALOG, serialize_upgrades
from .events import publish_event


class UpgradeStateView(generics.GenericAPIView):
    def get(self, request):
        return Response(serialize_upgrades(request.user.id))


class UpgradePurchaseView(generics.GenericAPIView):
    def post(self, request, upgrade_key):
        definition = UPGRADE_CATALOG.get(upgrade_key)
        if definition is None:
            return Response(
                {'detail': 'El upgrade solicitado no existe.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Solicitar descuento de puntos a game-service mediante endpoint interno seguro
        game_service_url = getattr(settings, 'GAME_SERVICE_URL', 'http://game-service:8002')
        internal_secret = getattr(settings, 'INTERNAL_API_SECRET', 'internal-shared-secret-key-123')

        try:
            resp = requests.post(
                f"{game_service_url}/api/v1/internal/deduct-points",
                headers={'X-Internal-Secret': internal_secret},
                json={
                    'user_id': request.user.id,
                    'cost': definition['cost'],
                    'nickname': request.user.nickname,
                },
                timeout=5,
            )
        except requests.RequestException as e:
            return Response(
                {'detail': f'Error comunicando con el servicio de progreso de juego: {str(e)}'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if resp.status_code != 200:
            data = resp.json() if resp.headers.get('content-type') == 'application/json' else {}
            return Response(
                {'detail': data.get('detail', 'No se pudo procesar la compra de puntos.')},
                status=resp.status_code,
            )

        new_score = resp.json().get('score', 0)

        # Registrar el incremento del upgrade en la base de datos de la tienda
        with transaction.atomic():
            upgrade, _ = PlayerUpgrade.objects.select_for_update().get_or_create(
                user_id=request.user.id,
                upgrade_type=upgrade_key,
            )
            upgrade.quantity += 1
            upgrade.save(update_fields=['quantity', 'updated_at'])

        # Emitir evento al bus
        publish_event('shop_events', {
            'event': 'upgrade_purchased',
            'user_id': request.user.id,
            'upgrade_type': upgrade_key,
            'quantity': upgrade.quantity,
        })

        return Response({
            'score': new_score,
            **serialize_upgrades(request.user.id),
        })
