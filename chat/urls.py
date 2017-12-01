# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from chat import views
urlpatterns = [
    # интерфейс манаджера:
    url(r'^management/$', views.management, name='management'),
    url(r'^management/dialog/(?P<dialog_id>\S+)/$', views.show_dialog, name='dialog'),
    url(r'^management/active/(?P<dialog_id>\S+)/$', views.close_dialog, name='close'),
    url(r'^management/logout$', views.logout_view, name='logout'),

    # интерфейс пользователя:
    url(r'^chat/$', views.client_dialog, name='show_client_dialog'),

    # работа с сообщениями:
    url(r'^messages/create/$', views.message_create, name='message_create'),
    url(r'^messages/get/$', views.messages_get, name='messages_get'),
    url(r'^messages/read/$', views.messages_read, name='messages_read'),
    url(r'^messages/seen/$', views.messages_get_first, name='messages_get_first'),

]

