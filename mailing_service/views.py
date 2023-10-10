from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Mailing, Message, Client


# Create your views here.
# class ContextViewMixin:
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         return context_data
#
#     def form_valid(self, form):
#         self.object = form.save()
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)


class HandleNoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.info(self.request, 'Для доступа к этой странице необходимо авторизоваться')
        return super().handle_no_permission()


class AddPermissionReuiredMixin(PermissionRequiredMixin):
    permission_required = 'mailing_service.'


def home(request):
    return render(request, 'mailing_service/home.html')


class MailingCreateView(HandleNoPermissionMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_service.add_mailing'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def form_valid(self, form):
        # self.object = form.save()
        # self.object.user = self.request.user
        # self.object.save()
        return super().form_valid(form)


class MailingUpdateView(HandleNoPermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_service.change_mailing'

    def get_success_url(self):
        return reverse('mailing_service:mailing_detail', args=[self.kwargs.get('pk')])


class MailingListView(HandleNoPermissionMixin, ListView):
    model = Mailing


class MailingDetailView(HandleNoPermissionMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = 'mailing_service.view_mailing'


class MailingDeleteView(HandleNoPermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing_service.delete_mailing'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MessageCreateView(HandleNoPermissionMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing_service.add_message'


class MessageUpdateView(HandleNoPermissionMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing_service.change_message'

    def get_success_url(self):
        return reverse('mailing_service:message_detail', args=[self.kwargs.get('pk')])


class MessageListView(HandleNoPermissionMixin, ListView):
    model = Message


class MessageDeleteView(HandleNoPermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'mailing_service.delete_message'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDetailView(HandleNoPermissionMixin, PermissionRequiredMixin, DetailView):
    model = Message
    permission_required = 'mailing_service.view_message'


class ClientCreateView(HandleNoPermissionMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing_service.add_client'
    success_url = reverse_lazy('mailing_service:client_list')


class ClientUpdateView(HandleNoPermissionMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing_service.change_client'

    def get_success_url(self):
        return reverse('mailing_service:client_detail', args=[self.kwargs.get('pk')])


class ClientListView(HandleNoPermissionMixin, ListView):
    model = Client


class ClientDetailView(HandleNoPermissionMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'mailing_service.view_client'


class ClientDeleteView(HandleNoPermissionMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing_service.delete_client'
    success_url = reverse_lazy('mailing_service:client_list')

