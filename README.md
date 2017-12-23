# WebChat
Простой web chat с панелью администратора и возможносью интеграции любому к web сайту.

#### Install
Проект имеет 2 интерфейса взаимодействия.  

Установка серверной части:
```
# Клонирование проекта
(webchat) user@pc:~/workspace$ git clone git@github.com:ersul4ik/webchat.git
(webchat) user@pc:~/workspace/webchat$ cd ./workspace/webchat

# Установка зависимостей
(webchat) user@ps:~/workspace/webchat$ pip install -r requirements.txt 

# Файл с настройками проекта
(webchat) user@ps:~/workspace/webchat$ cp .env-example .env

# Создание базы данных, создаие пользователя, запуск сервера
(webchat) user@ps:~/workspace/webchat$ ./manage.py migrate
(webchat) user@ps:~/workspace/webchat$ ./manage.py createsuperuser
(webchat) user@ps:~/workspace/webchat$ ./manage.py runserver 127.0.0.1:8000
```

Установка клиентской части:  
Подгружаем стили
```
<link rel="stylesheet" href="http://127.0.0.1:8000/static/css/webchat.css">
```
внизу html странице подключаем скрипт
```
<script src="http://127.0.0.1:8000/static/js/webchat.js"></script>
```

И небольщой [примерчик](example.html).