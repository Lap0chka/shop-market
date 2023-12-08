from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

urlpatterns = [
    path("login", views.UserLoginView.as_view(), name='login'),
    path("register", views.UserRegistrationView.as_view(), name='register'),
    path("profile/<int:pk>", login_required(views.UserProfileView.as_view()), name='profile'),
    path("logout", LogoutView.as_view(), name='logout'),
    path("verify/<str:email>/<uuid:code>", views.EmailVerifacationView.as_view(), name='email_verifacation'),
]