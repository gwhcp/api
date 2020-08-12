from worker.queue.os_type import OsType


class VsftpdPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """VSFTPd Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """VSFTPd Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        return cls.validate_path(paths.get(cls.value()))
