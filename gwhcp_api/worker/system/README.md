# GWHCP Worker - System #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* system_create_group
    * group

    `python manage.py system_create_group groupname`

* system_create_group_quota
    * group
    * quota

    `python manage.py system_create_group_quota groupname 10`

* system_create_host
    * domain
    * ip

    `python manage.py system_create_host example.com 10.1.1.1`

* system_create_hostname
    * domain

    `python manage.py system_create_hostname example.com`

* system_create_ipaddress
    * ip
    * subnet

    `python manage.py system_create_ipaddress 10.1.1.1 32`

* system_create_user
    * user
    * group

    `python manage.py system_create_user username groupname`

* system_create_user_quota
    * user
    * quota

    `python manage.py system_create_user_quota username quota`

* system_delete_group
    * group

    `python manage.py system_delete_group groupname`

* system_delete_host
    * domain
    * ip

    `python manage.py system_delete_host example.com 10.1.1.1`

* system_delete_hostname

    `python manage.py system_delete_hostname`

* system_delete_ipaddress
    * ip
    * subnet

    `python manage.py system_delete_ipaddress 10.1.1.1 32`

* system_delete_user
    * user

    `python manage.py system_delete_user username`

#### Celery Tasks ####

* system.tasks.create_group
* system.tasks.create_host
* system.tasks.create_hostname
* system.tasks.create_ipaddress
* system.tasks.create_group_quota
* system.tasks.create_user
* system.tasks.create_user_quota
* system.tasks.delete_group
* system.tasks.delete_host
* system.tasks.delete_hostname
* system.tasks.delete_ipaddress
* system.tasks.delete_user