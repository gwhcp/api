# GWHCP Worker - Gunicorn #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* gunicorn_create_config
    * domain
    * user

    `python manage.py gunicorn_create_config example.com username`
    
* gunicorn_create_service
    * domain
    * user

    `python manage.py gunicorn_create_service example.com username`
    
* gunicorn_delete_config
    * domain

    `python manage.py gunicorn_delete_config example.com`
    
* gunicorn_delete_service
    * domain

    `python manage.py gunicorn_delete_service example.com`

#### Celery Tasks ####

* gunicorn.tasks.create_config
* gunicorn.tasks.create_service
* gunicorn.tasks.delete_config
* gunicorn.tasks.delete_service