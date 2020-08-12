from worker.queue.os_type import OsType


class ApachePath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """Apache Configuration Directory

        :return: str
        """

        paths = {
            1: '/etc/httpd/conf/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def errordoc_dir(cls):
        """Apache Error Docs Directory

        :return: str
        """

        paths = {
            1: '/usr/share/httpd/error/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def etc_dir(cls):
        """Apache Etc Directory
    
        :return: str
        """

        paths = {
            1: '/etc/httpd/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def extra_dir(cls):
        """Apache Extra Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/httpd/conf/extra/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def icon_dir(cls):
        """Apache Icons Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/httpd/icons/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """Apache Logs Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/httpd/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """Apache Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/httpd/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_dir(cls):
        """Apache Sites Directory
    
        :return: str
        """

        paths = {
            1: '/etc/httpd/sites/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_enabled_dir(cls):
        """Apache Sites Enabled Directory
    
        :return: str
        """

        paths = {
            1: '/etc/httpd/sites-enabled/'
        }

        return cls.validate_path(paths.get(cls.value()))
