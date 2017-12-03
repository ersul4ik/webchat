# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/management/"

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
    read_dialogs = Dialog.objects.filter(is_active=True, messages__read=True).exclude(
        manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(is_active=True, messages__read=False).filter(
        ~Q(messages__sender=request.user)).distinct()

    dialog = get_object_or_404(Dialog, id=dialog_id)
    form = MessageForm(request.POST or None, initial={'dialog': dialog, 'sender': request.user})

    return render(request, 'management.html', locals())


# деактивирование диалога
@login_required
def close_dialog(request, dialog_id):
    Dialog.objects.filter(id=dialog_id).update(is_active=False)
    return HttpResponseRedirect("/management/")


@login_required
def management(request):
    read_dialogs = Dialog.objects.filter(is_active=True).exclude(manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(messages__read=False).filter(~Q(messages__sender=request.user)).distinct()
    return render(request, 'management.html', locals())


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
def messages_get_first(request):
    dialog = Dialog.objects.filter(messages__read=False, messages__seen=False,
                                   is_active=True)
    context = ''
    for d in dialog:
        if request.user != d.message.sender:
            context += render_to_string('message_list.html', locals())
    return HttpResponse(context)


# получение сообщений от отправителя
def messages_get(request):
    dialog = get_object_or_404(Dialog, Q(client=request.user) | Q(manager=request.user),
                               is_active=True)
    context = ''
    for m in dialog.messages.filter(read=False):
        if request.user != m.sender:
            context += render_to_string('receive.html', locals())
    return HttpResponse(context)


@csrf_exempt
def messages_read(request):
    dialog = get_object_or_404(Dialog, Q(client=request.user) | Q(manager=request.user), is_active=True)
    dialog.messages.filter(read=False, seen=False).exclude(sender=request.user).update(read=True, seen=True)
    return HttpResponse('Все ок')


@csrf_exempt
def client_dialog(request):
    user = request.user
    if request.is_ajax():
        if not user.is_authenticated:
            user = create_user(request)
        dialog, _ = Dialog.objects.get_or_create(client=user, is_active=True)
        initial = {'dialog': dialog.id, 'sender': user.id, 'body': request.POST.get('body', '')}
        request.POST = initial
        return message_create(request)

    if user.is_authenticated:
        dialog, _ = Dialog.objects.get_or_create(client=user, is_active=True)

    return render(request, 'user_message.html', locals())


def create_user(request):
    u = {'first_name': request.POST.get('client_name', ''),
         'last_name': 'anonymous',
         'username': get_random_string(length=16)}
    user = User.objects.create(**u)
    login(request, user)
    user.username = request.session.session_key
    user.save()
    return user

