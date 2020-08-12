from worker.queue.os_type import OsType


class PhpPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """PHP-FPM Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/php/php-fpm.d/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def etc_dir(cls):
        """PHP Etc Directory
    
        :return: str
        """

        paths = {
            1: '/etc/php/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ini_dir(cls):
        """PHP Ini Directory
    
        :return: str
        """

        paths = {
            1: '/etc/php/conf.d'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """PHP-FPM Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def modules_dir(cls):
        """PHP Modules Directory
    
        :return: str
        """

        paths = {
            1: '/usr/lib/php/modules/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """PHP-FPM Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/php-fpm/'
        }

        return cls.validate_path(paths.get(cls.value()))
