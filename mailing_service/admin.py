from django.contrib import admin

from mailing_service.models import Mailing, Client, MailLogs, Message


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_name', 'start_date', 'time', 'frequency', 'status')
    list_filter = ('time', 'start_date', 'frequency', 'status',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email')
    list_filter = ('fullname', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')


@admin.register(MailLogs)
class MailLogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'status', 'server_response', 'mailing')
    list_filter = ('mailing', 'status', 'timestamp')
