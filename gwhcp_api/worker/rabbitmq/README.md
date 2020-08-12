# GWHCP Worker - RabbitMQ #

#### Release Information ####

* Version: 1.0.0

#### Available Commands and Required Variables ####
  
* rabbitmq_server_install

    `python manage.py rabbitmq_server_install`

* rabbitmq_server_uninstall

    `python manage.py rabbitmq_server_uninstall`

#### Celery Tasks ####

* rabbitmq.tasks.server_install
* rabbitmq.tasks.server_uninstall

#### RabbitMQ Configuration ####

```
rabbitmqctl add_user gwhcp password
rabbitmqctl add_vhost /
rabbitmqctl set_permissions -p / gwhcp ".*" ".*" ".*"
```