# GWHCP Worker - Bind #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* bind_create_domain
    * domain

    `python manage.py bind_create_domain example.com`

* bind_delete_domain
    * domain

    `python manage.py bind_delete_domain example.com`

* bind_rebuild_all

    `python manage.py bind_rebuild_all`

* bind_rebuild_domain
    * domain

    `python manage.py bind_rebuild_domain example.com`

* bind_reload_domain
    * domain

    `python manage.py bind_reload_domain example.com`

* bind_server_install

    `python manage.py bind_server_install`

* bind_server_uninstall

    `python manage.py bind_server_uninstall`

#### Celery Tasks ####

* bind.tasks.create_domain
* bind.tasks.delete_domain
* bind.tasks.rebuild_all
* bind.tasks.rebuild_domain
* bind.tasks.reload_domain
* bind.tasks.server_install
* bind.tasks.server_uninstall