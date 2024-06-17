from django.contrib import admin

from e_mail.models import Client, MailingSettings, MailingMessage, Logger


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email', 'description')


@admin.register(MailingSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'start_time', 'end_time', 'status')
    search_fields = ('client', 'status')
    list_filter = ('status',)


@admin.register(MailingMessage)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    search_fields = ('subject', 'message')


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'last_time_sending', 'status')
    search_fields = ('mailing',)