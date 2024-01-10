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
        fields = ('username', 'password')



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
        'class': 'custom-file-label',
    }), required=False)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'readonly': True

    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",'readonly': True
    }))
    new_email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
    }), required=False)
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Old Password"
    }), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "New password"
    }), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Confirm password"
    }), required=False)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email',
                  'new_email', 'old_password', 'password1', 'password2')


