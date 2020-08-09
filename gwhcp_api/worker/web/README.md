# GWHCP Worker - Web #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* web_create_domain
    * domain
    * user
    * group

    `python manage.py web_create_domain example.com username groupname`

* web_delete_domain
    * domain
    * user

    `python manage.py web_delete_domain example.com username`

* web_ssl_install
    * domain
    * user

    `python manage.py web_ssl_install example.com username`

* web_ssl_uninstall
    * domain
    * user

    `python manage.py web_ssl_uninstall example.com username`

#### Celery Tasks ####

* web.tasks.create_domain
* web.tasks.delete_domain
* web.tasks.ssl_install
* web.tasks.ssl_uninstall