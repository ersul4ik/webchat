# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _


class Dialog(models.Model):
    user = models.CharField(_('User session key'), max_length=24, blank=True, null=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    manager = models.CharField(_('Chief'), max_length=24, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s " % self.user

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    def __unicode__(self):
        return "%s " % self.user

    def get_dialog_title(self):
        return 'Диалог между "{}"'.format(self.user_name)


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="message")
    sender = models.CharField(max_length=25, verbose_name=_("Author"))
    text = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_formatted_create_datetime(self):
        return dj_date(self.created, settings.DATETIME_FORMAT)

    def __str__(self):
        return self.sender + "(" + self.get_formatted_create_datetime() + ") - '" + self.text

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __unicode__(self):
        return "%s " % self.sender + "(" + self.get_formatted_create_datetime() + ") - '" + self.text
