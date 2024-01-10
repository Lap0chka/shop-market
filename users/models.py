from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


def get_upload_path(instance, filename):
    # Формируем путь для сохранения изображения в подкаталоге с именем пользователя
    return f'users_image/{instance.username}/{filename}'


class User(AbstractUser):
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    is_verifacated_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for {self.user.username}'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=None)

    def __str__(self):
        return f'EmailVerifacation object for {self.user.email}'

    def send_verifacation_email(self):
        link = reverse('email_verifacation', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Account verification for {self.user.username}'
        message = 'To verify your account for {}, follow the link {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
