from django.db import models


class LeaderboardEntry(models.Model):
    user_id = models.BigIntegerField(unique=True, primary_key=True)
    nickname = models.CharField(max_length=40, db_index=True)
    profile_icon = models.CharField(max_length=500, blank=True, null=True)
    score = models.PositiveBigIntegerField(default=0, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', 'nickname']

    def __str__(self):
        return f"{self.nickname}: {self.score}"
