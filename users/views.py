import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import LoginView as BaseLoginView

from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm
from users.models import User


class LoginView(BaseLoginView):
    form_class = UserAuthenticationForm


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Сохранение объекта перед тем, как установить ему пароль
        token = ''.join(random.sample(string.digits + string.ascii_letters, 12))
        self.object.token = token
        self.object.is_active = False
        self.object.save()
        # url = f'''http://127.0.0.1:8000/users/verify/{token}'''

        # if form.is_valid():
        #     send_mail(
        #         subject='Подтверждение регистрации',
        #         message=f'''Вы успешно зарегистрировались, чтобы подтвердить почту перейдите по ссылке {url}.''',
        #         from_email=settings.EMAIL_HOST_USER,
        #         recipient_list=[self.object.email]
        #     )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
