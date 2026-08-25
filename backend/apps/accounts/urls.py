from django.urls import path
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .views import RegisterView,LoginView,RefreshView,LogoutView,MeView
urlpatterns=[path('auth/register',RegisterView.as_view()),path('auth/login',LoginView.as_view()),path('auth/refresh',RefreshView.as_view()),path('auth/logout',LogoutView.as_view()),path('users/me',MeView.as_view())]
