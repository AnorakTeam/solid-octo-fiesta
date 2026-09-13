import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class StatelessUser:
    """Usuario desacoplado basado únicamente en los claims del token JWT."""
    def __init__(self, user_id, nickname=None):
        self.id = user_id
        self.pk = user_id
        self.nickname = nickname or f"player_{user_id}"
        self.is_authenticated = True
        self.is_active = True

    def __str__(self):
        return f"StatelessUser(id={self.id}, nickname={self.nickname})"


class StatelessJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        raw_token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                raw_token,
                settings.JWT_SIGNING_KEY,
                algorithms=['HS256'],
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('El token ha expirado.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token inválido.')

        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('El token no contiene user_id.')

        nickname = payload.get('nickname')
        user = StatelessUser(user_id=user_id, nickname=nickname)
        return (user, raw_token)
