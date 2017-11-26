# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404

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
def show_dialog(request, dialog_id):
    read_dialogs = Dialog.objects.filter(is_active=True).exclude(manager__isnull=True).distinct()
    not_read_dialogs = Dialog.objects.filter(messages__read=False).filter(~Q(messages__sender=request.user)).distinct()

    dialog = get_object_or_404(Dialog, id=dialog_id)
    form = MessageForm(request.POST or None, initial={'dialog': dialog, 'sender': request.user})

    return render(request, 'management.html', locals())


# def logout_a(request):
#     auth.logout(request)
#     return redirect('login')
#
#
# def login_a(request):
#     template = 'login.html'
#     form = LoginForm(data=request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             auth.login(request, form.get_user())
#             return redirect('')
#     return render(request, template, {'form': form})

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
        print(form.instance.read)

    dialog = form.instance.dialog
    if not dialog.manager and dialog.client != request.user:
        dialog.manager = request.user
        dialog.save()

    Message.objects.filter(dialog=dialog, read=False).exclude(sender=request.user).update(read=True)
    context = render_to_string('sent.html', {'m': form.instance})
    return HttpResponse(context)


@csrf_exempt
def client_dialog(request):
    user = request.user
    if request.is_ajax():
        if not user.is_authenticated:
            user = create_user(request)

        dialog, _ = Dialog.objects.get_or_create(client=user, is_active=True)
        print(dialog.manager)
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


# получение сообщений от оператора
def messages_get(request):
    dialog = get_object_or_404(Dialog, Q(client=request.user) | Q(manager=request.user), is_active=True)
    context = ''
    for m in dialog.messages.filter(read=False):
        if request.user != m.sender:
            context += render_to_string('receive.html', locals())
    return HttpResponse(context)


@csrf_exempt
def messages_read(request):
    dialog = get_object_or_404(Dialog, Q(client=request.user) | Q(manager=request.user), is_active=True)
    dialog.messages.filter(read=False).exclude(sender=request.user).update(read=True)
    return HttpResponse('Все ок')
