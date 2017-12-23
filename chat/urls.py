# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from chat import views
urlpatterns = [
    # интерфейс менаджера:
    url(r'management/$', views.management, name='management'),
    url(r'management/dialog/(?P<dialog_id>\S+)/$', views.show_dialog, name='dialog'),
    url(r'management/active/(?P<dialog_id>\S+)/$', views.close_dialog, name='close'),
    url(r'management/logout$', views.logout_view, name='logout'),

    # итерфейс супервизора:
    url(r'supervisor/$', views.staff_management, name='management'),
    url(r'management/operator/$', views.show_operators, name='show_operators'),
    url(r'management/operator/(?P<operator_id>\S+)/$', views.show_operator_room, name='show_operator_room'),
    url(r'management/dialog/(?P<dialog_id>\S+)/$', views.show_dialog, name='dialog'),
    url(r'management/active/(?P<dialog_id>\S+)/$', views.close_dialog, name='close'),
    url(r'management/deactive/(?P<operator_id>\S+)/$', views.operator_drop, name='operator_drop'),

    # интерфейс пользователя:
    url(r'chat/$', views.client_dialog, name='show_client_dialog'),

    # работа с сообщениями:
    url(r'messages/create/$', views.message_create, name='message_create'),
    url(r'messages/get/$', views.messages_get, name='messages_get'),
    url(r'messages/read/$', views.messages_read, name='messages_read'),
    url(r'messages/seen/$', views.messages_get_first, name='messages_get_first'),
    url(r'messages/receive/$', views.messages_following_get, name='messages_following_get'),

    # тестовый
    url(r'urmat/$', views.testing, name='testing'),
]
