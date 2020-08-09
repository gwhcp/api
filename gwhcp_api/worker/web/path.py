from worker.queue.os_type import OsType


class WebPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def ssl_dir(cls, user):
        """Web SSL Directory
    
        :param str user: Username
    
        :return: str
        """

        return cls.validate_path(cls.www_dir(user) + 'ssl/')

    @classmethod
    def www_dir(cls, user):
        """Virtual Hosts Directory
    
        :param str user: Username
    
        :return: str
        """

        return cls.validate_path('/home/' + user + '/')
