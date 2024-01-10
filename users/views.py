from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from users.form import UserProfileForm, UserRegisterForm, LoginForm
from users.models import EmailVerification, User
import uuid
from datetime import timedelta
from django.utils.timezone import now
# Create your views here.


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # После успешного входа выполните свои дополнительные действия
        return response
<<<<<<< HEAD
=======

>>>>>>> 6dfd8e8572edda4ad3568f3629be84484d9f6ee3


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Congratulations you have successfully registered'


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        old_password = form.cleaned_data.get('old_password')
        new_password1 = form.cleaned_data.get('password1')
        new_password2 = form.cleaned_data.get('password2')
        email = form.cleaned_data.get('new_email')

        if old_password and new_password1 and new_password2:
            # Проверяем и обновляем пароль, если предоставлен
            if self.request.user.check_password(old_password) and new_password1 == new_password2:
                self.request.user.set_password(new_password1)
                self.request.user.save()
                messages.success(self.request, 'Your password was successfully updated!')
            else:
                if not self.request.user.check_password(old_password):
                    messages.error(self.request, 'Incorrect old password. Please try again.')
                else:
                    messages.error(self.request, 'New passwords do not match. Please try again.')
                return self.form_invalid(form)
        elif email:
            # Обновляем email, если предоставлен
            self.request.user.email = email
            self.request.user.save()
            expiration = now() + timedelta(hours=24)
            record = EmailVerification.objects.create(code=uuid.uuid4(), user=self.request.user, expiration=expiration)
            record.send_verifacation_email()
            messages.success(self.request, 'Your email was successfully updated! Please confirm your new email address')


        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))

class EmailVerifacationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verifacated_email = True
            user.save()
            return super(EmailVerifacationView, self).get(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


