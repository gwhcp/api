import os
import shutil

from rest_framework import serializers

from worker.queue.os_type import OsType


class DovecotPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """Dovecot Config Directory
    
        :return: str
        """

        paths = {
            1: '/etc/dovecot/conf.d/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def etc_dir(cls):
        """Dovecot Etc Directory
    
        :return: str
        """

        paths = {
            1: '/etc/dovecot/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def log_dir(cls):
        """Dovecot Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def quota_warning_cmd(cls):
        """Dovecot Quota Warning Script
    
        :return: str
        """

        paths = {
            1: '/usr/bin/quota-warning.sh'
        }

        return paths[cls.value()]

    @classmethod
    def run_dir(cls):
        """Dovecot Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/dovecot/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def sieve_cmd(cls):
        """Dovecot Sieve Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/sievec'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ssl_dir(cls):
        """Dovecot SSL Directory
    
        :return: str
        """

        paths = {
            1: '/etc/dovecot/ssl/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def tmp_dir(cls):
        """Dovecot Temp Directory
    
        :return: str
        """

        paths = {
            1: '/tmp/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]

    @classmethod
    def usrlib_dir(cls):
        """Dovecot Usr/Lib Directory
    
        :return: str
        """

        paths = {
            1: '/usr/lib/dovecot/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def varlib_dir(cls):
        """Dovecot Var/Lib Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/dovecot/'
        }

        try:
            cls.validate_path(paths.get(cls.value()))
        except serializers.ValidationError:
            os.makedirs(paths.get(cls.value()), 0o755)

            shutil.chown(paths.get(cls.value()), user='root', group='root')

        return paths[cls.value()]
