# GWHCP Worker - Nginx #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* nginx_create_indexes_config
    * domain
    * user
    * indexes

    `python manage.py nginx_create_indexes_config example.com username index.htm index.html`

* nginx_create_logs_config
    * domain
    * user

    `python manage.py nginx_create_logs_config example.com username`

* nginx_create_python3_config
    * domain
    * user

    `python manage.py nginx_create_python3_config example.com username`

* nginx_create_virtual_config
    * domain
    * ip
    * port (80 / 443)
    * user

    `python manage.py nginx_create_virtual_config example.com 10.1.1.1 80 username`

* nginx_delete_indexes_config
    * domain

    `python manage.py nginx_delete_indexes_config example.com`

* nginx_delete_logs_config
    * domain

    `python manage.py nginx_delete_logs_config example.com`

* nginx_delete_python3_config
    * domain

    `python manage.py nginx_delete_python3_config example.com`

* nginx_delete_virtual_config
    * domain
    * port (80 / 443)

    `python manage.py nginx_delete_virtual_config example.com 80`

* nginx_disable_domain
    * domain

    `python manage.py nginx_disable_domain example.com`

* nginx_enable_domain
    * domain

    `python manage.py nginx_enable_domain example.com`

* nginx_server_install

    `python manage.py nginx_server_install`

* nginx_server_uninstall

    `python manage.py nginx_server_uninstall`

#### Celery Tasks ####

* nginx.tasks.create_indexes_config
* nginx.tasks.create_logs_config
* nginx.tasks.create_python3_config
* nginx.tasks.create_virtual_config
* nginx.tasks.delete_indexes_config
* nginx.tasks.delete_logs_config
* nginx.tasks.delete_python3_config
* nginx.tasks.delete_virtual_config
* nginx.tasks.disable_domain
* nginx.tasks.enable_domain
* nginx.tasks.server_install
* nginx.tasks.server_uninstall