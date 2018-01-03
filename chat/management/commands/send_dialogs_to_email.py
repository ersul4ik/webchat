# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from chat.models import Dialog
from django.core.mail import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        dialogs = Dialog.objects.filter(is_active=False)
        for dialog in dialogs:
            title = u'{} и {}'.format(dialog.client.first_name, dialog.manager)
            messages = dialog.messages.all()
            message = ''
            for mess in messages:
                message += u'{} - {}'.format(mess.sender, mess.body) + u'\n'
            send_mail(title, message, settings.EMAIL_HOST_USER, ['ersul4ik@mail.ru'], fail_silently=True)
