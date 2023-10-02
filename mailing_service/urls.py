from django.urls import path

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import home

app_name = MailingServiceConfig.name

urlpatterns = [
    path('', home, name='home'),
]