from django.db import models


class PlayerUpgrade(models.Model):
    class Type(models.TextChoices):
        CLICKER = 'clicker', 'Clicker'
        STATIC = 'static', 'Static'
        SPAMMER = 'spammer', 'Spammer'

    user_id = models.BigIntegerField(db_index=True)
    upgrade_type = models.CharField(max_length=20, choices=Type.choices)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user_id', 'upgrade_type'),
                name='unique_shop_player_upgrade',
            ),
        ]

    def __str__(self):
        return f"PlayerUpgrade(user_id={self.user_id}, type={self.upgrade_type}, qty={self.quantity})"
