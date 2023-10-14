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
        exclude = ('user', 'status')
        help_texts = {
            'clients': 'Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений.',
        }
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MessageForm(FormClassMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('user',)


class ClientForm(FormClassMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)
