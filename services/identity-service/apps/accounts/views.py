from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .events import publish_event


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    pass


class MeView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.UpdateAPIView):
    """Actualiza el usuario autenticado, emitiendo evento para el leaderboard."""
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        icon_url = (
            self.request.build_absolute_uri(user.profile_icon.url)
            if user.profile_icon else None
        )
        publish_event('user_events', {
            'event': 'profile_updated',
            'user_id': user.id,
            'nickname': user.nickname,
            'profile_icon': icon_url,
        })


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            RefreshToken(request.data['refresh']).blacklist()
        except Exception:
            pass
        return Response(status=204)
