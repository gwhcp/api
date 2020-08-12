from worker.queue.os_type import OsType


class NginxPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """Nginx Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/nginx/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_dir(cls):
        """Nginx Sites Directory
    
        :return: str
        """

        paths = {
            1: '/etc/nginx/sites/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_conf_dir(cls):
        """Nginx Sites Conf Directory
    
        :return: str
        """

        paths = {
            1: '/etc/nginx/sites-conf/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_enabled_dir(cls):
        """Nginx Sites Enabled Directory
    
        :return: str
        """

        paths = {
            1: '/etc/nginx/sites-enabled/'
        }

        return cls.validate_path(paths.get(cls.value()))
