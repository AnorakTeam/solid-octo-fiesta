from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from .serializers import RegisterSerializer, UserSerializer
class RegisterView(generics.CreateAPIView): queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]
class LoginView(TokenObtainPairView): pass
class RefreshView(TokenRefreshView): pass
class MeView(generics.RetrieveAPIView):
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
    
class LogoutView(generics.GenericAPIView):
    def post(self,request):
        try: RefreshToken(request.data['refresh']).blacklist()
        except Exception: pass
        return Response(status=204)
