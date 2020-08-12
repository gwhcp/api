from worker.queue.os_type import OsType


class AwstatsPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def base_dir(cls):
        """AWStats Base Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/webapps/awstats/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def cgi_bin_dir(cls):
        """AWStats cgi-bin Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/webapps/awstats/cgi-bin/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def classes_dir(cls):
        """AWStats Classes Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/webapps/awstats/classes/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def css_dir(cls):
        """AWStats CSS Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/webapps/awstats/css/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def icon_dir(cls):
        """AWStats Icon Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/webapps/awstats/icon/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sites_dir(cls):
        """AWStats Site Directory
    
        :return: str
        """

        paths = {
            1: '/etc/awstats/sites/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def tools_dir(cls):
        """AWStats Tools Directory
    
        :return: str
        """

        paths = {
            1: '/usr/share/awstats/tools/'
        }

        return cls.validate_path(paths.get(cls.value()))
