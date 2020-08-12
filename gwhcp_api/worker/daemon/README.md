# GWHCP Worker - Daemon #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* daemon_celery_install
    * domain
    * ip

    `python manage.py daemon_celery_install example.com 10.1.1.1`

* daemon_celery_uninstall

    `python manage.py daemon_celery_uninstall`

* daemon_ipaddress
    * command (start / stop)

    `python manage.py daemon_ipaddress start`

* daemon_ipaddress_install
    * domain

    `python manage.py daemon_ipaddress_install example.com`

* daemon_ipaddress_uninstall

    `python manage.py daemon_ipaddress_uninstall`

* daemon_worker
    * command (start / stop)

    `python manage.py daemon_worker start`

* daemon_worker_install
    * domain

    `python manage.py daemon_worker_install example.com`

* daemon_worker_uninstall

    `python manage.py daemon_worker_uninstall`

#### Celery Tasks ####

* daemon.tasks.celery_install
* daemon.tasks.celery_uninstall
* daemon.tasks.ipaddress_install
* daemon.tasks.ipaddress_uninstall
* daemon.tasks.worker_install
* daemon.tasks.worker_uninstall