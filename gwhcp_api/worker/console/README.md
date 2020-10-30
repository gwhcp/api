# GWHCP Worker - Console #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* console_service
    * action (disable / enable / restart / start / stop)
    * service (cronie / dovecot / httpd / mariadb / named / nginx / php-fpm / postfix / postgresql / prosody / rabbitmq / uwsgi / vsftpd)

    `python manage.py console_service enable nginx`

#### Celery Tasks ####

* console.tasks.ders