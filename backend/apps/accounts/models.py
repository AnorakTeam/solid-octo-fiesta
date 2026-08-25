from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra):
        if not email: raise ValueError('email is required')
        user=self.model(email=self.normalize_email(email),**extra); user.set_password(password); user.save(); return user
    def create_superuser(self,email,password=None,**extra):
        extra.update(is_staff=True,is_superuser=True); return self.create_user(email,password,**extra)
class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True); nickname=models.CharField(max_length=40,unique=True); is_active=models.BooleanField(default=True); is_staff=models.BooleanField(default=False); date_joined=models.DateTimeField(auto_now_add=True)
    objects=UserManager(); USERNAME_FIELD='email'; REQUIRED_FIELDS=[]
