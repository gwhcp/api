# GWHCP Worker - AWStats #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* awstats_create_auth
    * domain
    * user
    * password

    `python manage.py awstats_create_auth example.com username password`

* awstats_create_domain
    * domain
    * user
    * ip
    * ip_type (namebased / dedicated)

    `python manage.py awstats_create_domain example.com username 10.1.1.1 dedicated`

* awstats_delete_domain
    * domain

    `python manage.py awstats_delete_domain example.com`

* awstats_update_all

    `python manage.py awstats_update_all`

* awstats_update_domain
    * domain

    `python manage.py awstats_update_domain example.com`

#### Celery Tasks ####

* awstats.tasks.create_auth
* awstats.tasks.create_domain
* awstats.tasks.delete_domain
* awstats.tasks.update_all
* awstats.tasks.update_domain