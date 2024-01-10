from users.models import Profile  # Импортируйте вашу модель Profile

def create_profile(backend, user, *args, **kwargs):
    """Создать профиль пользователя для социальной аутентификации """
<<<<<<< HEAD
    profile, created = Profile.objects.get_or_create(user=user)
    # Добавьте дополнительные действия, если нужно
=======
    profile, created = Profile.objects.get_or_create(user=user)
>>>>>>> 6dfd8e8572edda4ad3568f3629be84484d9f6ee3
