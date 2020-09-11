from django.apps import AppConfig


class Config(AppConfig):
    label = 'company.xmpp'

    name = label

    verbose_name = 'Company XMPP'
