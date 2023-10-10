from django import forms

from mailing_service.models import Mailing, Message, Client


class FormClassMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(FormClassMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('mailing_name', 'time', 'frequency', 'clients', 'message')
        help_texts = {
            'clients': 'Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений.',
        }
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MessageForm(FormClassMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(FormClassMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
