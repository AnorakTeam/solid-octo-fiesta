from rest_framework import serializers
from .models import PlayerProgress
class ProgressSerializer(serializers.ModelSerializer):
    class Meta: model=PlayerProgress; fields=('score','updated_at'); read_only_fields=('updated_at',)
class LeaderboardSerializer(serializers.Serializer):
    position=serializers.IntegerField(); nickname=serializers.CharField(); score=serializers.IntegerField(); profile_icon=serializers.URLField(allow_null=True)
