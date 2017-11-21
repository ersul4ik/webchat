# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Dialog, Message


class DialogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dialog._meta.fields]


admin.site.register(Dialog, DialogAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'dialog',
        'sender',
        'text',
        'read'
    )
    list_filter = ('created', 'dialog', 'sender', 'read')


admin.site.register(Message, MessageAdmin)
