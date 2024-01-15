from users.models import Profile  # Импортируйте вашу модель Profile
from users.models import EmailVerification, User
import uuid
from datetime import timedelta
from django.utils.timezone import now


def create_profile(backend, user, *args, **kwargs):
    """Создать профиль пользователя для социальной аутентификации """
    profile, created = Profile.objects.get_or_create(user=user)
    if not user.is_verifacated_email:
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verifacation_email()


