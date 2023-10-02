from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mailing_service.models import Mailing


# Create your views here.


def home(request):
    return render(request, 'mailing_service/base.html')


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('time', 'frequency', 'clients')
    # success_url = reverse_lazy()


