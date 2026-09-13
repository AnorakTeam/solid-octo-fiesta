from rest_framework import serializers
from .models import PlayerProgress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProgress
        fields = ('score', 'updated_at')
