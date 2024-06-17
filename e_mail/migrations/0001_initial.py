# Generated by Django 4.2.13 on 2024-06-15 15:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Почта"
                    ),
                ),
                ("first_name", models.CharField(max_length=10, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=10, verbose_name="Фамилия")),
                (
                    "patronymic",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Отчество"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Logger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_time_sending",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Время рассылки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[(True, "Успешно"), (False, "Неудача")],
                        default=False,
                        max_length=30,
                        null=True,
                        verbose_name="Попытка",
                    ),
                ),
            ],
            options={
                "verbose_name": "лог",
                "verbose_name_plural": "логи",
            },
        ),
        migrations.CreateModel(
            name="MailingMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(max_length=100, verbose_name="Тема письма"),
                ),
                ("message", models.TextField(verbose_name="Текст письма")),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="MailingSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mailing_name",
                    models.CharField(
                        default="mailing_name",
                        max_length=50,
                        verbose_name="Название рассылки",
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("per_day", "раз в день"),
                            ("per_week", "раз в неделю"),
                            ("per_month", "раз в месяц"),
                        ],
                        default="per_month",
                        max_length=12,
                        verbose_name="Периодичность рассылки",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "создана"),
                            ("executing", "запущена"),
                            ("finished", "закончена успешно"),
                            ("error", "законечена с ошибками"),
                        ],
                        default="created",
                        max_length=15,
                        verbose_name="Статус рассылки",
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Начало рассылки",
                    ),
                ),
                (
                    "end_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Конец рассылки"
                    ),
                ),
                (
                    "next_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата следующей рассылки",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="Активна"),
                ),
                (
                    "client",
                    models.ManyToManyField(
                        to="e_mail.client", verbose_name="Получатель"
                    ),
                ),
                (
                    "mail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="e_mail.mailingmessage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройка",
                "verbose_name_plural": "Настройки",
                "permissions": [("toggle_active", "выключить рассылку")],
            },
        ),
    ]
