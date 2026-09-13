from django.db import models


class PlayerProgress(models.Model):
    user_id = models.BigIntegerField(unique=True, db_index=True)
    score = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PlayerProgress(user_id={self.user_id}, score={self.score})"
