from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Mailing, Message, Client


# Create your views here.
class ContextViewMixin:

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def home(request):
    return render(request, 'mailing_service/home.html')


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    # success_url = reverse_lazy()


class MessageCreateView(CreateView):
    model = Message
    # fields = ('subject', 'body')
    form_class = MessageForm


class MessageUpdateView(UpdateView):
    model = Message
    # fields = ('subject', 'body')
    form_class = MessageForm


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    # success_url = reverse_lazy()


class MessageDetailView(DetailView):
    model = Message


class ClientCreateView(CreateView):
    model = Client
    # fields = ('fullname', 'email', 'comment')
    form_class = ClientForm


class ClientUpdateView(UpdateView):
    model = Client
    # fields = ('fullname', 'email', 'comment')
    form_class = ClientForm


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    # success_url = reverse_lazy()

