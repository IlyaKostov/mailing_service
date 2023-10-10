from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from mailing_service.forms import FormClassMixin
from users.models import User


class UserRegisterForm(FormClassMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(FormClassMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country', 'birthday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserAuthenticationForm(FormClassMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
