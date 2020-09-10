from django.apps import AppConfig


class Config(AppConfig):
    label = 'employee.mail'

    name = label

    verbose_name = 'Employee Mail'
