#Команды, выполненные на сервере
    1.sudo apt-get install postgresql
    2.sudo apt-get install postgresql-server-dev-all
    3.sudo -u postgres psql postgres
        a. \password postgres
        b. Ввёл пароль: 300896
        c. Создал пользователя denis
            ```sql
            create user denis with password '300896';
            alter role denis set client_encoding to 'utf8';
            alter role denis set default_transaction_isolation to 'read committed';
            alter role denis set timezone to 'UTC';
        d. create database yandex_school_db owner denis;
        e. Вышел из postgres (\q)
    4.   
## Установка virtualenv
    1. sudo pip3 install virtualenv 
    2. sudo pip3 install virtualenvwrapper
    3. В ~/.bashrc дописываем:
        a.export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
        b.source /usr/bin/virtualenvwrapper.sh
    4. Перезапускаем пользователя
##Настройка тестов
    1.sudo -u postgres psql postgres
    2.ALTER USER denis CREATEDB;
    3. Далее тесты вызаваются командой: ./manage.py test
