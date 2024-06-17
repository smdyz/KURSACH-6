from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}

LOG_CHOICES = (
    (True, 'Успешно'),
    (False, 'Неудача'),
)


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    first_name = models.CharField(max_length=10, verbose_name='Имя')
    last_name = models.CharField(max_length=10, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Владелец клиента', **NULLABLE)

    def __str__(self):
        return f'{self.email}: ({self.first_name}, {self.last_name}, {self.description})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Текст письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Владелец письма', **NULLABLE)

    def __str__(self):
        return f'{self.subject}; {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    period_variants = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )
    status_variants = (
        ('created', 'создана'),
        ('executing', 'запущена'),
        ('finished', 'закончена успешно'),
        ('error', 'законечена с ошибками')
    )
    mailing_name = models.CharField(max_length=50, verbose_name='Название рассылки', default='mailing_name')
    client = models.ManyToManyField(Client, verbose_name='Получатель')
    mail = models.ForeignKey(MailingMessage, on_delete=models.CASCADE)
    period = models.CharField(max_length=12, default='per_month', choices=period_variants,
                              verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=15, choices=status_variants, default='created', verbose_name='Статус рассылки')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='Начало рассылки')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='Конец рассылки')
    next_date = models.DateTimeField(default=timezone.now, verbose_name='Дата следующей рассылки')
    is_active = models.BooleanField(default=False, verbose_name='Активна')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='Владелец рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.client}: ({self.start_time} - {self.end_time}; {self.status})'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
        permissions = [
            (
                'toggle_active',
                'выключить рассылку'
            ),
        ]


class Logger(models.Model):
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_time_sending = models.DateTimeField(auto_now=True, verbose_name='Время рассылки', **NULLABLE)
    status = models.CharField(default=False, max_length=30, choices=LOG_CHOICES, verbose_name='Попытка', **NULLABLE)

    def __str__(self):
        return f'{self.last_time_sending} - {self.status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

