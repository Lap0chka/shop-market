from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from users.form import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification, User

# Create your views here.


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


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

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance = request.user,data=request.POST,files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {'form':form,'basket':Basket.objects.filter(user=request.user)}
#     return render(request,'users/profile.html',context)

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Congratulations you have successfully registered')
#             return HttpResponseRedirect(reverse('login'))
#     else:
#         form = UserRegisterForm
#     context = {'form':form}
#     return render(request,'users/register.html',context)
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username,password=password)
#             if user:
#                 auth.login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form':form}
#     return render(request,'users/login.html',context)
