import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Mailing, Message, Client


class UserQuerysetMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class StaffUserObjectMixin:

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class UserObjectMixin:

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class UserFormMixin:

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ObjectStatusMixin:

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.start_date == datetime.date.today():
            self.object.status = Mailing.Status.RUNNING
        else:
            self.object.status = Mailing.Status.CREATED
        self.object.save()
        return super().form_valid(form)


class LoginRequiredMessageMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, 'Для доступа к этой странице необходимо авторизоваться')
        return super().handle_no_permission()


def home(request):
    return render(request, 'mailing_service/home.html')


class MailingCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin,
                        ObjectStatusMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_service.add_mailing'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        return form


class MailingUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin,
                        UserObjectMixin, ObjectStatusMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_service.change_mailing'

    def get_success_url(self):
        return reverse('mailing_service:mailing_detail', args=[self.kwargs.get('pk')])


class MailingListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Mailing
    permission_required = 'mailing_service.view_mailing'


class MailingDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Mailing
    permission_required = 'mailing_service.view_mailing'


class MailingDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Mailing
    permission_required = 'mailing_service.delete_mailing'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MessageCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing_service.add_message'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing_service.change_message'

    def get_success_url(self):
        return reverse('mailing_service:message_detail', args=[self.kwargs.get('pk')])


class MessageListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Message
    permission_required = 'mailing_service.view_message'


class MessageDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Message
    permission_required = 'mailing_service.delete_message'
    success_url = reverse_lazy('mailing_service:message_list')


class MessageDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Message
    permission_required = 'mailing_service.view_message'


class ClientCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing_service.add_client'
    success_url = reverse_lazy('mailing_service:client_list')


class ClientUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin,  UserObjectMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing_service.change_client'

    def get_success_url(self):
        return reverse('mailing_service:client_detail', args=[self.kwargs.get('pk')])


class ClientListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Client
    permission_required = 'mailing_service.view_client'


class ClientDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Client
    permission_required = 'mailing_service.view_client'


class ClientDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Client
    permission_required = 'mailing_service.delete_client'
    success_url = reverse_lazy('mailing_service:client_list')

