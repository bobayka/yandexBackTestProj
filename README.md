# Yandex REST API

Для создания REST API использовались:
 - [Django](https://www.djangoproject.com/) 
 - [Django REST framework](https://www.django-rest-framework.org/)
 -  объектно-реляционная СУБД [PostgreSQL](https://www.postgresql.org/)
 -  web-сервер [Gunicorn](https://gunicorn.org/) - WSGI сервер для UNIX


## Команды, выполненные на сервере
### Настройка Postgresql
    1. sudo apt-get install postgresql
    2. sudo apt-get install postgresql-server-dev-all
    3. sudo -u postgres psql postgres
        a. \password postgres
        b. Пароль: 300896
        c. Создал пользователя denis
            ```sql
            create user denis with password '300896';
            alter role denis set client_encoding to 'utf8';
            alter role denis set default_transaction_isolation to 'read committed';
            alter role denis set timezone to 'UTC';
        d. create database yandex_school_db owner denis;
        e. Выйти из postgres (\q)   

### Клонирование репозитория
    1. sudo apt install git
    2. cd ~/project 
    3. git clone git@github.com:bobayka/yandexBackTestProj.git 
    Проект теперь находится в ~/project/yandexBackTestProj
### Установка virtualenv
    1. sudo apt-get install python3-venv
    2. python3 -m venv venv
    3. Из папки проекта  source ./venv/bin/activate
    4. pip3 install -r requirements.txt
### Настройка проекта 
    1. ./manage.py makemigrations
    2. ./manage.py migrate
### Развёртывание сайта
    1. pip install gunicorn   
    2. Из папки проекта gunicorn -b :8080 OnlineStoreREST.wsgi 
### Настройка тестов
    1.sudo -u postgres psql postgres
    2.ALTER USER denis CREATEDB;
    3. Далее тесты вызаваются командой: ./manage.py test
