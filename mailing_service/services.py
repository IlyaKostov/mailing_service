from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog


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
