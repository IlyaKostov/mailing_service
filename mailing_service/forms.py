from django import forms

from mailing_service.models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('time', 'frequency', 'clients', 'message')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
