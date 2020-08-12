# GWHCP Worker - Cron #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* cron_create_config
    * domain
    * user
    * cron_id

    `python manage.py cron_create_config example.com username 1`

* cron_create_domain
    * domain
    * user

    `python manage.py cron_create_domain example.com username`

* cron_delete_config
    * domain
    * user
    * cron_id

    `python manage.py cron_delete_config example.com username 1`

* cron_delete_domain
    * domain
    * user

    `python manage.py cron_delete_domain example.com username`

#### Celery Tasks ####

* cron.tasks.create_config
* cron.tasks.create_domain
* cron.tasks.delete_config
* cron.tasks.delete_domain