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

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def etc_dir(cls):
        """Dovecot Etc Directory
    
        :return: str
        """

        paths = {
            1: '/etc/dovecot/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """Dovecot Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def quota_warning_cmd(cls):
        """Dovecot Quota Warning Script
    
        :return: str
        """

        paths = {
            1: '/usr/bin/quota-warning.sh'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """Dovecot Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/dovecot/'
        }

        return cls.validate_path(paths.get(cls.value()))

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

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def tmp_dir(cls):
        """Dovecot Temp Directory
    
        :return: str
        """

        paths = {
            1: '/tmp/'
        }

        return cls.validate_path(paths.get(cls.value()))

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

        return cls.validate_path(paths.get(cls.value()))
