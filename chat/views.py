# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.forms import Form
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from chat.forms import LoginForm

from django.template.context_processors import csrf

from chat.models import *


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/chief/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class MessageForm(Form):
    class Meta:
        model = Message


@login_required
def chief(request):
    dialog_list = Dialog.objects.filter(message__read=True).distinct()
    messages_not_view = Message.objects.filter(read=False).distinct()
    return render(request, "chat_list.html", locals())


def user_template(request):
    template = 'user_message.html'
    session = request.session
    if not session.get('my_key'):
        session.cycle_key()
        session['my_key'] = session.session_key
    dialog, _ = Dialog.objects.get_or_create(user=session.session_key, is_active=True)  # реализация комнаты
    dialog.user_name = request.POST.get('sender')
    dialog.save()

    init = {'sender': dialog.user, 'dialog': dialog}
    form = MessageForm(request.POST or None, initial=init)
    if form.is_valid():
        s = request.POST.get('sender', '')
        t = request.POST.get('text', '')
        message = {'dialog': dialog, 'text': t, 'sender': s}
        m = Message.objects.create(**message)
        if request.is_ajax():
            return render(request, 'sent.html', {'m': m})
    return render(request, template, locals())


@login_required
def show_dialog(request, dialog_id):
    dialog = get_object_or_404(Dialog, id=dialog_id)
    template = "chat_list.html"
    form = MessageForm(request.POST or None)
    if form.is_valid():
        s = request.POST.get('sender', '')
        t = request.POST.get('text', '')
        message = {'dialog': dialog, 'text': t, 'sender': s}
        Message.objects.create(**message)
        dialog.manager = request.user.username
        dialog.save()
        dialog.message.update(read=True)
        # form.save()
    return render(request, template, locals())


def logout_a(request):
    auth.logout(request)
    return redirect('login')


def login_a(request):
    template = 'login.html'
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('')
    return render(request, template, {'form': form})
