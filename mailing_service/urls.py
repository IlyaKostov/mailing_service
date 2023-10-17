from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import *

app_name = MailingServiceConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/<int:pk>/toggle_activity', toggle_activity, name='mailing_toggle_activity'),
    path('logs/', MailLogsListView.as_view(), name='logs'),
    path('logs/<int:pk>/', get_mailing_logs, name='mailing_logs')
]
