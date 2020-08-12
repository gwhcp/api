# GWHCP Worker - PHP #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* php_create_config
    * domain
    * user
    * group

    `python manage.py php_create_config example.com username groupname`

* php_delete_config
    * user

    `python manage.py php_delete_config username`

* php_server_install

    `python manage.py php_server_install`

* php_server_uninstall

    `python manage.py php_server_uninstall`

#### Celery Tasks ####

* php.tasks.create_config
* php.tasks.delete_config
* php.tasks.server_install
* php.tasks.server_uninstall