from worker.queue.os_type import OsType

from worker.web.path import WebPath


class CronPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def base_dir(cls, user):
        """Cron Directory

        :param str user: Username

        :return: str
        """

        return cls.validate_path(f"{WebPath.www_dir(user)}cron/")

    @classmethod
    def domain_dir(cls, user):
        """Cron Domain Directory

        :param str user: Username

        :return: str
        """

        return cls.validate_path(f"{cls.base_dir(user)}domain/")
