from worker.queue.os_type import OsType


class BindPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def rndc_cmd(cls):
        """RNDC Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/rndc'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def conf_dir(cls):
        """Bind Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def domain_dir(cls):
        """Bind Domain Directory
    
        :return: str
        """

        paths = {
            1: '/var/named/domain/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ipaddress_dir(cls):
        """Bind Reverse IP Address Directory
    
        :return: str
        """

        paths = {
            1: '/var/named/ipaddress/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """Bind Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """Bind Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/named/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def var_dir(cls):
        """Bind Var Directory
    
        :return: str
        """

        paths = {
            1: '/var/named/'
        }

        return cls.validate_path(paths.get(cls.value()))
