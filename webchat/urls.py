# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin

from chat import views

urlpatterns = [
    url(r'^chief/', admin.site.urls),
    url(r'^', include('chat.urls')),
    url(r'^register/$', views.register),
    url(r'^login/$', views.LoginFormView.as_view()),
]
