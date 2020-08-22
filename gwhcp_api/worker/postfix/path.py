import os
import shutil

from rest_framework import serializers

from worker.queue.os_type import OsType


class PostfixPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def command_dir(cls):
        """Postfix Command Directory
    
        :return: str
        """

        paths = {
            1: '/usr/bin/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def conf_dir(cls):
        """Postfix Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/postfix/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def daemon_dir(cls):
        """Postfix Daemon Directory
    
        :return: str
        """

        paths = {
            1: '/usr/lib/postfix/bin/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def data_dir(cls):
        """Postfix Data Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/postfix/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def newaliases_cmd(cls):
        """Postfix newaliases Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/newaliases'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def queue_dir(cls):
        """Postfix Queue Directory
    
        :return: str
        """

        paths = {
            1: '/var/spool/postfix/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sendmail_cmd(cls):
        """Postfix sendmail Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/sendmail'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ssl_dir(cls):
        """Postfix SSL Directory
    
        :return: str
        """

        paths = {
            1: '/etc/postfix/ssl/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]
