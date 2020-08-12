# GWHCP Worker - eJabberD #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* ejabberd_server_install
    * domain
    * ip

    `python manage.py ejabberd_server_install example.com 10.1.1.1`

* ejabberd_server_uninstall

    `python manage.py ejabberd_server_uninstall`

#### Celery Tasks ####

* ejabberd.tasks.server_install
* ejabberd.tasks.server_uninstall