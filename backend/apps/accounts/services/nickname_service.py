from django.db import IntegrityError
from ..models import User
def generate_nickname(email):
    base=email.split('@')[0].lower().replace('.','')[:30] or 'player'; candidate=base; number=0
    while User.objects.filter(nickname=candidate).exists():
        number += 1; candidate=f'{base}{number}'[:40]
    return candidate
