import random

from django.conf import settings


class ReadWrite:
    """
    Handles all models associated with the respected database.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to 'default_read' database.
        """

        db_choice = []

        for item in settings.DATABASES:
            if item.startswith('default_read'):
                db_choice.append(item)

        if len(db_choice) > 0:
            return random.choice(db_choice)

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to 'default' database.
        """

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations.
        """

        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations.
        """

        return db == 'default'
