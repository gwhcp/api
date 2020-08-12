# GWHCP Worker - Dovecot #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* dovecot_create_config_ssl
    * domain

    `python manage.py dovecot_create_config_ssl example.com`

* dovecot_server_install

    `python manage.py dovecot_server_install`

* dovecot_server_uninstall

    `python manage.py dovecot_server_uninstall`

#### Celery Tasks ####

* dovecot.tasks.create_config_ssl
* dovecot.tasks.server_install
* dovecot.tasks.server_uninstall