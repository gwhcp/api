# GWHCP Worker - Apache #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* apache_create_config
    * domain
    * ip (80 / 443)
    * port
    * user
    * group

    `python manage.py apache_create_config example.com 10.1.1.1 80 username groupname`

* apache_delete_config
    * domain
    * port (all / 80 / 443)

    `python manage.py apache_delete_config example.com 80`

* apache_disable_domain
    * domain

    `python manage.py apache_disable_domain example.com`

* apache_enable_domain
    * domain

    `python manage.py apache_enable_domain example.com`

* apache_server_install

    `python manage.py apache_server_install`

* apache_server_uninstall

    `python manage.py apache_server_uninstall`

#### Celery Tasks ####

* apache.tasks.create_config
* apache.tasks.delete_config
* apache.tasks.disable_domain
* apache.tasks.enable_domain
* apache.tasks.server_install
* apache.tasks.server_uninstall