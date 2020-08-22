from django.apps import AppConfig


class Config(AppConfig):
    label = 'employee.account'

    name = label

    verbose_name = 'Employee Account'
