from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing_service.models import Mailing, Message, Client


# Create your views here.


def home(request):
    return render(request, 'mailing_service/home.html')


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('time', 'frequency', 'clients', 'message')
    # success_url = reverse_lazy()


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('time', 'frequency', 'clients','message')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    # success_url = reverse_lazy()


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body')


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    # success_url = reverse_lazy()


class MessageDetailView(DetailView):
    model = Message


class ClientCreateView(CreateView):
    model = Client
    fields = ('fullname', 'email', 'comment')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('fullname', 'email', 'comment')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    # success_url = reverse_lazy()

