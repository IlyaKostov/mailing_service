from django.contrib.auth import get_user_model
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    fullname = models.CharField(max_length=200, verbose_name='ФИО')
    email = models.EmailField(verbose_name='контактный email')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ('-id',)


class Mailing(models.Model):

    class Frequency(models.TextChoices):
        DAILY = 'daily', 'Раз в день'
        WEEKLY = 'weekly', 'Раз в неделю'
        MONTHLY = 'monthly', 'Раз в месяц'

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Завершена'
        CREATED = 'created', 'Создана'
        RUNNING = 'running', 'Запущена'

    mailing_name = models.CharField(max_length=200, verbose_name='название рассылки')
    start_date = models.DateField(verbose_name='дата рассылки')
    time = models.TimeField(verbose_name='время рассылки')
    frequency = models.CharField(max_length=15, choices=Frequency.choices, verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED, verbose_name='статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='сообщение')
    is_active = models.BooleanField(default=True, verbose_name='активность рассылки')

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_name}({self.pk}): {self.get_frequency_display()}, {self.get_status_display()}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('-id',)
        permissions = [
            (
                'change_activity',
                'Change activity'
            )
        ]


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name='тема письма', **NULLABLE)
    body = models.TextField(verbose_name='тело письма', **NULLABLE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('-id',)


class MailLogs(models.Model):

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Успешно'
        FAILURE = 'failure', 'Ошибка'

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f'{self.mailing} - {self.timestamp} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
        ordering = ('-id',)
