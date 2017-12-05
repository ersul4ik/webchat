# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _


class Dialog(models.Model):
    client = models.ForeignKey(User, verbose_name=_('Client'), related_name='dialogs')
    manager = models.ForeignKey(User, verbose_name=_('Manager'), null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    def __unicode__(self):
        manager = ''
        if self.manager:
            manager = self.manager.first_name
        return '{} и {}'.format(self.client.first_name, manager)

    def get_dialog_title(self):
        return 'Чат c "{}"'.format(self.client.first_name)

    # def get_manager(self):
    #     manager = self.manager
    #     manager = random.choice
    #     return manager


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialogs"), related_name="messages")
    sender = models.ForeignKey(User, verbose_name=_("Sender"))
    body = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    seen = models.BooleanField(verbose_name=_("Seen"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_formatted_create_datetime(self):
        return dj_date(self.created_at, settings.DATETIME_FORMAT)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __unicode__(self):
        return "{} ({}) - '{}'".format(self.sender.first_name, self.get_formatted_create_datetime(), self.body)
