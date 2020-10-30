from worker.queue.os_type import OsType


class GunicornPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """Gunicorn Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/gunicorn/'
        }

        return cls.validate_path(paths.get(cls.value()))
