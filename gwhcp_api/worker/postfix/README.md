# GWHCP Worker - Postfix #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* postfix_server_install
    * service (sendmail / server / server_ssl)

    `python manage.py postfix_server_install sendmail`

* postfix_server_uninstall

    `python manage.py postfix_server_uninstall`

#### Celery Tasks ####

* postfix.tasks.server_install
* postfix.tasks.server_uninstall