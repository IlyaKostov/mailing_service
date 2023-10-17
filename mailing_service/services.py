import calendar
import datetime

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from mailing_service.models import MailLogs, Mailing


def get_random_blog_article():
    if settings.CACHE_ENABLED:
        key = 'blog_article'
        blog_article = cache.get(key)
        if blog_article is None:
            blog_article = Blog.objects.order_by('?')[:3]
            cache.set(key, blog_article)
    else:
        blog_article = Blog.objects.order_by('?')[:3]
    return blog_article


def add_users_group_permissions(group):
    """Добавление разрешений в группу users"""
    permissions = Permission.objects.filter(content_type__model__in=['mailing', 'message', 'client'])
    for perm in permissions:
        group.permissions.add(perm)


def send_verify_mail(url, email):
    """Сообщение о подтверждении электронной почты, после регистрации"""
    send_mail(
        subject='Подтверждение регистрации',
        message=f'''Вы успешно зарегистрировались, чтобы подтвердить почту перейдите по ссылке {url}.''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def new_password_mail(email, password):
    """Сообщение с паролем, при сбросе"""
    send_mail(
        subject='Сброс пароля',
        message=f'''Вы успешно сбросили пароль для аккаунта {email}.\n Ваш новый пароль: {password}''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def my_job():
    today = datetime.datetime.now()
    time_now = today.strftime('%H:%M')
    date_today = today.date()
    mailings_today = Mailing.objects.filter(start_date=date_today, is_active=True, status=Mailing.Status.CREATED)

    for mailing in mailings_today:
        mailing_time = mailing.time.strftime('%H:%M')
        print(mailing)

        if mailing_time <= time_now:
            mailing.status = mailing.Status.RUNNING
            mailing.save()

            clients = mailing.clients.all()
            recipient_list = [client.email for client in clients]
            try:
                response = send_mail(mailing.message.subject, mailing.message.body, settings.EMAIL_HOST_USER,
                                     recipient_list)
                if response:
                    log = MailLogs(mailing=mailing, status=MailLogs.Status.SUCCESS, server_response=response)
                else:
                    log = MailLogs(mailing=mailing, status=MailLogs.Status.FAILURE, server_response=response)
                log.save()
            except Exception as response:
                log = MailLogs(mailing=mailing, status=MailLogs.Status.FAILURE, server_response=response)
                log.save()

            if mailing.frequency == Mailing.Frequency.DAILY:
                mailing.start_date = date_today + datetime.timedelta(days=1)
            elif mailing.frequency == Mailing.Frequency.WEEKLY:
                mailing.start_date = date_today + datetime.timedelta(days=7)
            elif mailing.frequency == Mailing.Frequency.MONTHLY:
                days_in_month = calendar.monthrange(today.year, today.month)[1]
                mailing.start_date = date_today + datetime.timedelta(days=days_in_month)

            mailing.status = mailing.Status.CREATED
            mailing.save()
