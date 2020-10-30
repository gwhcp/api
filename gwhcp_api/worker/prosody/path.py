from worker.queue.os_type import OsType


class ProsodyPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """Prosody Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/prosody/'
        }

        return cls.validate_path(paths.get(cls.value()))
