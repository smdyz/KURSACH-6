from django.db import models

from e_mail.models import NULLABLE


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок', **NULLABLE)
    body = models.TextField(verbose_name='Содержимое', **NULLABLE)
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    publish_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return f'{self.title}: {self.views_count}, {self.publish_date}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        permissions = [
            (
                'can_toggle_published',
                'изменить статус публикации'
            )
        ]

