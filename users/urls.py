from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('verify/<str:token>/', verify_email, name='verify'),
    # path('reset_password/', reset_password, name='reset_password'),
]
