import re
from rest_framework import serializers
from .models import User
from .services.nickname_service import generate_nickname
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta: model=User; fields=('email','password','nickname'); read_only_fields=('nickname',)
    def create(self,validated):
        user=User.objects.create_user(validated['email'],validated['password'],nickname=generate_nickname(validated['email'])); from apps.game.models import PlayerProgress; PlayerProgress.objects.create(user=user); return user
class UserSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=('id','email','nickname')


class ProfileSerializer(serializers.ModelSerializer):
    """Perfil público del jugador; nunca expone credenciales ni progreso."""
    profile_icon = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'profile_icon')
        read_only_fields = ('id', 'email')

    def validate_nickname(self, value):
        nickname = value.strip().lower()
        if not re.fullmatch(r'[a-z0-9_]{3,40}', nickname):
            raise serializers.ValidationError('Usa entre 3 y 40 caracteres: letras, números o guion bajo.')
        if User.objects.filter(nickname__iexact=nickname).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Este nickname ya está en uso.')
        return nickname

    def validate_profile_icon(self, value):
        if value is None:
            return value
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('El ícono no puede superar 2 MB.')
        allowed_types = {'image/jpeg', 'image/png', 'image/webp'}
        if getattr(value, 'content_type', '') not in allowed_types:
            raise serializers.ValidationError('Usa una imagen JPG, PNG o WebP.')
        return value
