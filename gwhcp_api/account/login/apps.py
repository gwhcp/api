from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class Config(AppConfig):
    label = 'account.login'

    name = label

    verbose_name = 'Login'

    def ready(self):
        from account.login import signals

        user_logged_in.connect(signals.handle_login)
