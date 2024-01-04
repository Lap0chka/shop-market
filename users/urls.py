from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from users import views

urlpatterns = [

    path("register/", views.UserRegistrationView.as_view(), name='register'),
    path("profile/<int:pk>", login_required(views.UserProfileView.as_view()), name='profile'),
    path('', include('django.contrib.auth.urls')),
    path("verify/<str:email>/<uuid:code>", views.EmailVerifacationView.as_view(), name='email_verifacation'),


]
