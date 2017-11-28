# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from chat.models import Dialog, Message


@admin.register(Dialog)
class RoomAdmin(admin.ModelAdmin):
    exclude = ()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    exclude = ()
    list_filter = ('created_at', 'dialog', 'sender', 'read', 'seen')
