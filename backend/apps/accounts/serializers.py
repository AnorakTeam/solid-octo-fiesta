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
