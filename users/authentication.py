from users.models import User

def create_profile(backend, user, *args, **kwargs):
    """Создать профиль пользователя для социальной аутентификации """
    User.objects.get_or_create(user=user)