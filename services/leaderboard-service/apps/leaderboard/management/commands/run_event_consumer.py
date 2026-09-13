import json
import logging
import os
import time
import redis
from django.core.management.base import BaseCommand
from apps.leaderboard.models import LeaderboardEntry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Escucha eventos de Redis para mantener actualizada la proyección del Leaderboard'

    def handle(self, *args, **options):
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
        self.stdout.write(self.style.SUCCESS(f"==> Iniciando consumidor de eventos en {redis_url}"))

        while True:
            try:
                client = redis.Redis.from_url(redis_url)
                pubsub = client.pubsub()
                pubsub.subscribe('game_events', 'user_events')
                self.stdout.write(self.style.SUCCESS("==> Suscrito exitosamente a 'game_events' y 'user_events'"))

                for message in pubsub.listen():
                    if message['type'] != 'message':
                        continue

                    try:
                        data = json.loads(message['data'])
                        event_type = data.get('event')

                        if event_type == 'score_updated':
                            user_id = data.get('user_id')
                            nickname = data.get('nickname')
                            score = int(data.get('score', 0))

                            entry, created = LeaderboardEntry.objects.get_or_create(
                                user_id=user_id,
                                defaults={'nickname': nickname, 'score': score}
                            )
                            if not created:
                                if score > entry.score:
                                    entry.score = score
                                if nickname:
                                    entry.nickname = nickname
                                entry.save()

                        elif event_type == 'profile_updated':
                            user_id = data.get('user_id')
                            nickname = data.get('nickname')
                            profile_icon = data.get('profile_icon')

                            entry, created = LeaderboardEntry.objects.get_or_create(
                                user_id=user_id,
                                defaults={'nickname': nickname or f"player_{user_id}", 'score': 0, 'profile_icon': profile_icon}
                            )
                            if not created:
                                if nickname:
                                    entry.nickname = nickname
                                if profile_icon is not None:
                                    entry.profile_icon = profile_icon
                                entry.save()

                        elif event_type == 'user_registered':
                            user_id = data.get('user_id')
                            nickname = data.get('nickname')
                            LeaderboardEntry.objects.get_or_create(
                                user_id=user_id,
                                defaults={'nickname': nickname, 'score': 0}
                            )

                    except Exception as e:
                        logger.error(f"Error procesando mensaje de evento: {e}")

            except redis.ConnectionError as e:
                self.stdout.write(self.style.WARNING(f"Conexión a Redis perdida ({e}). Reintentando en 3s..."))
                time.sleep(3)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Excepción en consumidor: {e}. Reintentando en 3s..."))
                time.sleep(3)
