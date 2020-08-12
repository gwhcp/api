# GWHCP Worker - MySQL #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* mysql_create_database
    * database

    `python manage.py mysql_create_database example`

* mysql_create_user
    * user
    * password

    `python manage.py mysql_create_user username password`

* mysql_delete_database
    * database

    `python manage.py mysql_delete_database example`

* mysql_delete_user
    * user

    `python manage.py mysql_delete_user username`

* mysql_disable
    * database
    * user

    `python manage.py mysql_disable example username`

* mysql_enable
    * database
    * user
    * Option Arguments
        * --select=(Y/N)
        * --insert=(Y/N)
        * --update=(Y/N)
        * --delete=(Y/N)
        * --create=(Y/N)
        * --alter=(Y/N)
        * --drop=(Y/N)
        * --index=(Y/N)
        * --create-view=(Y/N)
        * --show-view=(Y/N)

    `python manage.py mysql_enable example username --select=Y --insert=N`

* mysql_password
    * user
    * password

    `python manage.py mysql_password username password`

* mysql_permission
    * database
    * user
    * Option Arguments
        * --select=(Y/N)
        * --insert=(Y/N)
        * --update=(Y/N)
        * --delete=(Y/N)
        * --create=(Y/N)
        * --alter=(Y/N)
        * --drop=(Y/N)
        * --index=(Y/N)
        * --create-view=(Y/N)
        * --show-view=(Y/N)

    `python manage.py mysql_permission example username --select=Y --insert=N`

* mysql_server_install

    `python manage.py mysql_server_install`

* mysql_server_uninstall

    `python manage.py mysql_server_uninstall`

#### Celery Tasks ####

* mysql.tasks.create_database
* mysql.tasks.create_user
* mysql.tasks.delete_database
* mysql.tasks.delete_user
* mysql.tasks.disable
* mysql.tasks.enable
* mysql.tasks.password
* mysql.tasks.permission
* mysql.tasks.server_install
* mysql.tasks.server_uninstall