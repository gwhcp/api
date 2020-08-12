# GWHCP Worker - PostgreSQL #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* postgresql_create_database
    * database
    * user

    `python manage.py postgresql_create_database example username`

* postgresql_create_user
    * user
    * password

    `python manage.py postgresql_create_user username password`

* postgresql_delete_database
    * database

    `python manage.py postgresql_delete_database example`

* postgresql_delete_user
    * database
    * user
    * owner

    `python manage.py postgresql_delete_user example username admin`

* postgresql_disable
    * database
    * user
    * owner

    `python manage.py postgresql_disable example username admin`

* postgresql_enable
    * database
    * user
    * owner  
    * Optional Arguments
        * --select=(Y / N)
        * --insert=(Y / N)
        * --update=(Y / N)
        * --delete=(Y / N)
        * --truncate=(Y / N)
        * --references=(Y / N)
        * --trigger=(Y / N)

    `python manage.py postgresql_enable example username admin --select=Y --insert=N`

* postgresql_password
    * user
    * password

    `python manage.py postgresql_password username password`

* postgresql_permission
    * database
    * user
    * owner  
    * Optional Arguments
        * --select=(Y / N)
        * --insert=(Y / N)
        * --update=(Y / N)
        * --delete=(Y / N)
        * --truncate=(Y / N)
        * --references=(Y / N)
        * --trigger=(Y / N)

    `python manage.py postgresql_permission example username admin --select=Y --insert=N`

* postgresql_server_install

    `python manage.py postgresql_server_install`

* postgresql_server_uninstall

    `python manage.py postgresql_server_uninstall`

#### Celery Tasks ####

* postgresql.tasks.create_database
* postgresql.tasks.create_user
* postgresql.tasks.delete_database
* postgresql.tasks.delete_user
* postgresql.tasks.disable
* postgresql.tasks.enable
* postgresql.tasks.password
* postgresql.tasks.permission
* postgresql.tasks.server_install
* postgresql.tasks.server_uninstall