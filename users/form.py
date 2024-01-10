import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (UserChangeForm,
                                       UserCreationForm, AuthenticationForm)
from django.utils.timezone import now

from users.models import EmailVerification, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Password"
    }))

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('username', 'password')

=======
        fields = ('username', 'password',)
>>>>>>> 6dfd8e8572edda4ad3568f3629be84484d9f6ee3

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': "First name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Second name"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Username"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Email"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Confirm password"
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=True)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verifacation_email()
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "custom-file-label",
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'readonly': True

    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'readonly': True
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


