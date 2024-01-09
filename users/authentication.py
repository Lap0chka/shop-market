from users.models import Profile  # Импортируйте вашу модель Profile

def create_profile(backend, user, *args, **kwargs):
    """Создать профиль пользователя для социальной аутентификации """
    profile, created = Profile.objects.get_or_create(user=user)