from django.apps import AppConfig


class Config(AppConfig):
    label = 'employee.manage'

    name = label

    verbose_name = 'Employee Manage'
