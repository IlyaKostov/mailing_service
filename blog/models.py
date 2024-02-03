from django.db import models

from mailing_service.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title} ({self.created_at})'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
