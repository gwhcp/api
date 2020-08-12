from worker.queue.os_type import OsType


class PostgresqlPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def archive_dir(cls):
        """Postgres Archive Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/postgres/archive/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def data_dir(cls):
        """Postgres Data Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/postgres/data/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def database_dir(cls):
        """Postgres Database Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/postgres/databases/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def initdb_cmd(cls):
        """Postgres initdb Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/initdb'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def psql_cmd(cls):
        """Postgres psql Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/psql'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """Postgres Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/postgresql/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def user_dir(cls):
        """Postgres User Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/postgres/users/'
        }

        return cls.validate_path(paths.get(cls.value()))
