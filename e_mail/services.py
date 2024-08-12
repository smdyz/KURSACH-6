import pytz
from datetime import timedelta, datetime

from django.core.cache import cache

from blog.models import Blog
from config import settings
from django.core.mail import send_mail

from e_mail.models import MailingSettings, MailingMessage, Client, Logger


def my_job():
    day = timedelta(days=1)
    week = timedelta(days=7)
    month = timedelta(days=31)

    zone = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(zone)
    mailings = MailingSettings.objects.all().filter(is_active=True)

    for mailing in mailings:
        if mailing.status != 'finished':
            mailing.status = 'executing'
            mailing.save()
            emails_list = [client.email for client in mailing.client.all()]

            print(f'Рассылка {mailing.id} - начало {mailing.start_time}; конец {mailing.end_time}')

            result = send_mail(
                subject=mailing.mail.subject,
                message=mailing.mail.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_list
            )
            print('Пошла рассылка')

            status = result == True

            log = Logger(mailing=mailing, status=status)
            log.save()

            if mailing.period == 'per_day':
                mailing.next_date = log.last_time_sending + day
            elif mailing.period == 'per_week':
                mailing.next_date = log.last_time_sending + week
            elif mailing.period == 'per_month':
                mailing.next_date = log.last_time_sending + month

            if status:  # на случай сбоя рассылки она останется активной
                if mailing.next_date < mailing.end_time:
                    mailing.status = 'created'
                else:
                    mailing.status = 'finished'

            mailing.save()
            print(f'Рассылка {mailing.mailing_name} отправлена {today} (должна была {mailing.next_date})')


def get_cache_mailing_active():
    if settings.CACHE_ENABLED:
        key = 'mailing_quantity_active'
        mailing_quantity_active = cache.get(key)
        if mailing_quantity_active is None:
            mailing_quantity_active = MailingSettings.objects.filter(is_active=True).count()
            cache.set(key, mailing_quantity_active)
    else:
        mailing_quantity_active = MailingSettings.objects.all().count()
    return mailing_quantity_active


def get_mailing_count_from_cache():
    if settings.CACHE_ENABLED:
        key = 'mailing_quantity'
        mailing_quantity = cache.get(key)
        if mailing_quantity is None:
            mailing_quantity = MailingSettings.objects.all().count()
            cache.set(key, mailing_quantity)
    else:
         mailing_quantity = MailingSettings.objects.all().count()
    return mailing_quantity


def get_cache_unique_quantity():
    if settings.CACHE_ENABLED:
        key = 'clients_unique_quantity'
        clients_unique_quantity = cache.get(key)
        if clients_unique_quantity is None:
            clients_unique_quantity = len(list(set(Client.objects.all())))
            cache.set(key, clients_unique_quantity)
    else:
        clients_unique_quantity = len(list(set(Client.objects.all())))

    return clients_unique_quantity


def home_page_caching():
    if settings.CACHE_ENABLED:
        key = f'mails_list'
        mails_list = cache.get(key)
        if mails_list is None:
            mails_list = MailingMessage.objects.all()
            cache.set(key, mails_list)
    else:
        mails_list = MailingMessage.objects.all()

    return mails_list

