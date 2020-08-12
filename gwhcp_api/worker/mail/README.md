# GWHCP Worker - Mail #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####

* mail_create_domain
    * domain

    `python manage.py mail_create_domain example.com`

* mail_create_forward
    * domain
    * user
    * email

    `python manage.py mail_create_forward example.com username example@example.com`

* mail_create_list
    * domain
    * user
    * hostname

    `python manage.py mail_create_list example.com username mail.example.com`

* mail_create_mailbox
    * domain
    * user
    * password
    * quota

    `python manage.py mail_create_mailbox example.com username password 10`

* mail_delete_domain
    * domain

    `python manage.py mail_delete_domain example.com`

* mail_delete_forward
    * domain
    * user

    `python manage.py mail_delete_forward example.com username`

* mail_delete_list
    * domain
    * user

    `python manage.py mail_delete_list example.com username`

* mail_delete_mailbox
    * domain
    * user

    `python manage.py mail_delete_mailbox example.com username`

* mail_disable
    * domain
    * user

    `python manage.py mail_disable example.com username`

* mail_enable
    * domain
    * user

    `python manage.py mail_enable example.com username`

* mail_update_forward
    * domain
    * user
    * email

    `python manage.py mail_update_forward example.com username example@example.com`

* mail_update_mailbox
    * domain
    * user
    * password
    * quota

    `python manage.py mail_update_mailbox example.com username password 10`

#### Celery Tasks ####

* mail.tasks.create_domain
* mail.tasks.create_forward
* mail.tasks.create_list
* mail.tasks.create_mailbox
* mail.tasks.delete_domain
* mail.tasks.delete_forward
* mail.tasks.delete_list
* mail.tasks.delete_mailbox
* mail.tasks.disable
* mail.tasks.enable
* mail.tasks.update_forward
* mail.tasks.update_mailbox