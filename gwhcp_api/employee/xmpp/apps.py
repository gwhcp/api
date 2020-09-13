from django.apps import AppConfig


class Config(AppConfig):
    label = 'employee.xmpp'

    name = label

    verbose_name = 'Employee XMPP'
