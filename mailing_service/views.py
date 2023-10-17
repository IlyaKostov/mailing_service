from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Mailing, Message, Client, MailLogs
from mailing_service.services import get_random_blog_article


class UserQuerysetMixin:
    """Ограничивает список просматриваемых пользователем объектов, принадлежащими только текущему пользователю,
     и сохраняет доступ для персонала"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class StaffUserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам, и сохраняет доступ для персонала"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class UserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class UserFormMixin:
    """Присваивает объект пользователю который его создал"""

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LoginRequiredMessageMixin(LoginRequiredMixin):
    """Ограничение доступа только для авторизованных пользователей, вывод соответствующего информационного сообщения"""

    def handle_no_permission(self):
        messages.error(self.request, 'Для доступа к этой странице необходимо авторизоваться')
        return super().handle_no_permission()


def home(request):
    all_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(is_active=True,
                                             status__in=[Mailing.Status.CREATED, Mailing.Status.RUNNING]).count()
    clients = Client.objects.all().values('email').distinct().count()
    random_blog_article = get_random_blog_article()
    context = {
        'all_mailings': all_mailings,
        'active_mailings': active_mailings,
        'clients': clients,
        'blog_list': random_blog_article,
    }
    return render(request, 'mailing_service/home.html', context=context)


class MailingCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing_service.add_mailing'
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_form(self, form_class=None):
        """Формирование полей 'clients' и 'message' в форме, принадлежащих текущему пользователю"""
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)
        return form


class MailingUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
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


class ClientUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
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


@login_required
@permission_required('mailing_service.change_activity')
def toggle_activity(request, pk):
    """Отключение рассылок"""
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.user.is_staff:
        if mailing.is_active:
            mailing.is_active = False
            mailing.status = mailing.Status.COMPLETED
            mailing.save()
        else:
            mailing.is_active = True
            mailing.status = mailing.Status.CREATED
            mailing.save()
        return redirect('mailing_service:mailing_list')


class MailLogsListView(LoginRequiredMessageMixin, ListView):
    model = MailLogs

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(mailing__user=self.request.user)


@login_required
def get_mailing_logs(request, pk):
    mailing_logs = MailLogs.objects.filter(mailing_id=pk)
    mailing = mailing_logs.first().mailing
    context = {
        'object_list': mailing_logs,
        'mailing_name': mailing.mailing_name
    }
    return render(request, 'mailing_service/mailing_logs.html', context=context)
