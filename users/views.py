import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import LoginView as BaseLoginView

from mailing_service.services import add_users_group_permissions, send_verify_mail, new_password_mail
from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm
from users.models import User


class LoginView(BaseLoginView):
    form_class = UserAuthenticationForm


class LogoutView(BaseLogoutView):
    pass


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_message = ('Вы успешно зарегистрировались, '
                       'чтобы подтвердить профиль перейдите по ссылке отправленной вам на почту.')
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Формирование и отправка токена для верификации пользователя"""
        self.object = form.save(commit=False)
        token = ''.join(random.sample(string.digits + string.ascii_letters, 12))
        self.object.token = token
        self.object.is_active = False
        group, created = Group.objects.get_or_create(name='user')
        if created:
            add_users_group_permissions(group)

        self.object.save()
        self.object.groups.add(group)
        url = f'''http://127.0.0.1:8000/users/verify/{token}'''

        if form.is_valid():
            send_verify_mail(url, self.object.email)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    """Сброс пароля"""
    if request.method == 'POST':
        input_email = request.POST.get('email')
        user = User.objects.filter(email=input_email).first()
        if user:
            password = ''.join(random.sample(string.digits + string.ascii_letters, 12))
            user.set_password(password)
            user.save()
            new_password_mail(input_email, password)
        else:
            messages.warning(request, 'Пользователь с таким email не найден')

    return render(request, 'users/reset_password.html')


def verify_email(request, token):
    """Подтверждение регистрации при использовании токена отправленного на почту пользователя"""
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()
        messages.success(request, 'Пользователь успешно подтвержден')
    else:
        messages.error(request, 'Пользователь не найден')
    return redirect('users:login')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'


@permission_required('users.set_activity')
@login_required
def toggle_activity(request, user_id):
    """Блокировка/Разблокировка пользователя"""
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_staff:
        if user.is_active and not user.is_superuser:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('users:list')

