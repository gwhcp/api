import random

from django.conf import settings


class ReadWrite:
    """
    Handles all models associated with the respected database.
    """

    __jabber_tables = (
        'archive',
        'archive_prefs',
        'bosh',
        'caps_features',
        'carboncopy',
        'groups',
        'irc_custom',
        'last',
        'motd',
        'muc_online_room',
        'muc_online_users',
        'muc_registered',
        'muc_room',
        'oauth_token',
        'privacy_default_list',
        'privacy_list',
        'privacy_list_data',
        'private_storage',
        'proxy65',
        'pubsub_item',
        'pubsub_node',
        'pubsub_node_option',
        'pubsub_node_owner',
        'pubsub_state',
        'pubsub_subscription_opt',
        'roster_version',
        'rostergroups',
        'rosterusers',
        'route',
        'sm',
        'spool',
        'sr_group',
        'sr_user',
        'users',
        'vcard',
        'vcard_search'
    )

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to 'default_read' or 'jabber_read' database.
        """

        db_choice = []

        if model._meta.db_table in self.__jabber_tables:
            for item in settings.DATABASES:
                if item.startswith('jabber_read'):
                    db_choice.append(item)
        else:
            for item in settings.DATABASES:
                if item.startswith('default_read'):
                    db_choice.append(item)

        if len(db_choice) > 0:
            return random.choice(db_choice)

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to 'default' or 'jabber' database.
        """

        if model._meta.db_table in self.__jabber_tables:
            return 'jabber'
        else:
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

        if app_label == 'jabber':
            return db == 'jabber'

        return db == 'default'
