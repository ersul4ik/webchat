# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, redirect

from chat.forms import MessageForm
from chat.models import Dialog, Message


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.first_name = form.data['first_name']
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/management/"
    user = None

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def show_dialog(request, dialog_id):
    read_dialogs = Dialog.objects.filter(is_active=True, messages__read=True,
                                         messages__sender=request.user).exclude(manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(is_active=True, messages__read=False).distinct()

    dialog = get_object_or_404(Dialog, id=dialog_id)
    if not dialog.manager:
        dialog.manager = request.user
        dialog.save()
    form = MessageForm(request.POST or None, initial={'dialog': dialog, 'sender': request.user})
    return render(request, 'management.html', locals())


@login_required
def management(request):
    read_dialogs = Dialog.objects.filter(is_active=True, messages__read=True,
                                         messages__sender=request.user).exclude(manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(is_active=True, messages__read=False).distinct()
    return render(request, 'management.html', locals())


@login_required
def staff_management(request):
    read_dialogs = Dialog.objects.filter(is_active=True, messages__read=True,
                                         ).exclude(manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(is_active=True, messages__read=False).distinct()
    return render(request, 'staff.html', locals())


def show_operators(request):
    all_operators = User.objects.filter(is_active=True)
    return render(request, 'management.html', locals())


def show_operator_room(request, operator_id):
    operator_detail = User.objects.filter(id=operator_id)
    dialog = Dialog.objects.filter(manager=operator_id).count()
    return render(request, 'management.html', locals())


def operator_drop(request, operator_id):
    User.objects.filter(id=operator_id, is_active=True).update(is_active=False)
    return HttpResponseRedirect("/management/operator/")


# деактивирование диалога
@login_required
def close_dialog(request, dialog_id):
    Dialog.objects.filter(id=dialog_id).update(is_active=False)
    return HttpResponseRedirect("/management/")


@login_required
def message_create(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        form.save()

    dialog = form.instance.dialog
    if not dialog.manager and dialog.client != request.user:
        dialog.manager = request.user
        dialog.save()

    Message.objects.filter(dialog=dialog, read=False).exclude(sender=request.user).update(read=True)
    context = render_to_string('sent.html', {'m': form.instance})
    return HttpResponse(context)


# получение сообщений в левой части интерфейса оператора
@csrf_exempt
def messages_get_first(request):
    dialog = Dialog.objects.filter(unexplored=True)
    context = ''
    for d in dialog:
        if not d.manager:
            context += render_to_string('message_list.html', locals())
            time.sleep(5)
            dialog.update(unexplored=False)
            Message.objects.filter(seen=False).update(seen=True)
    return HttpResponse(context)


def messages_following_get(request):
    new_mess_in_dialog = Dialog.objects.filter(unexplored=False, messages__seen=False)
    context = ''
    for mess in new_mess_in_dialog:
            context += render_to_string('following_messages.html', locals())
            Message.objects.filter(seen=False, read=False).update(seen=True, read=True)
    return HttpResponse(context)


# получение сообщений от отправителя
def messages_get(request):
    messages = Message.objects.filter(
        Q(dialog__client=request.user) | Q(dialog__manager=request.user),
        dialog__is_active=True, read=False)
    context = ''
    for m in messages:
        if request.user != m.sender:
            context += render_to_string('receive.html', locals())
    return HttpResponse(context)


@csrf_exempt
def messages_read(request):
    dialog = get_object_or_404(Dialog, Q(client=request.user) | Q(manager=request.user), is_active=True)
    dialog.messages.filter(read=False, seen=False).exclude(sender=request.user).update(read=True, seen=True)
    return HttpResponse('Все ок')


# @vary_on_headers('HTTP_X_REQUESTED_WITH')
@csrf_exempt
def client_dialog(request):
    user = request.user
    if not user.is_anonymous:
        dialog, _ = Dialog.objects.get_or_create(client=user, is_active=True)
    if 'create' in request.GET:
        if user.is_anonymous:
            user = create_user(request)
        dialog, _ = Dialog.objects.get_or_create(client=user, is_active=True)
        initial = {'dialog': dialog.id, 'sender': user.id, 'body': request.POST.get('body', '')}
        request.POST = initial
        return message_create(request)

    return render(request, 'user_message.html', locals())
# is_authenticated() vs. is_anonymous()


def create_user(request):
    u = {'first_name': request.POST.get('client_name', ''),
         'last_name': 'anonymous',
         'username': get_random_string(length=16)}
    user = User.objects.create(**u)
    login(request, user)
    user.username = request.session.session_key
    user.save()
    return user
