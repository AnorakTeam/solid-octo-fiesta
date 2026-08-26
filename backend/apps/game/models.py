from django.conf import settings
from django.db import models


class PlayerProgress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    score = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PlayerUpgrade(models.Model):
    class Type(models.TextChoices):
        CLICKER = 'clicker', 'Clicker'
        STATIC = 'static', 'Static'
        SPAMMER = 'spammer', 'Spammer'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_upgrades',
    )
    upgrade_type = models.CharField(max_length=20, choices=Type.choices)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'upgrade_type'),
                name='unique_player_upgrade_type',
            ),
        ]
