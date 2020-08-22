from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class Config(AppConfig):
    label = 'login'

    name = label

    verbose_name = 'Login'

    def ready(self):
        from login import signals

        user_logged_in.connect(signals.handle_login)
