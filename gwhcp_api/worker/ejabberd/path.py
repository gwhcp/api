from worker.queue.os_type import OsType


class EjabberdPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """eJabberD Configuration Directory

        :return: str
        """

        paths = {
            1: '/etc/ejabberd/'
        }

        return cls.validate_path(paths.get(cls.value()))
