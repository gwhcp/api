from worker.queue.os_type import OsType


class MysqlPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """MySQL Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/mysql/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def database_dir(cls):
        """MySQL Database Directory
    
        :return: str
        """

        paths = {
            1: '/etc/mysql/databases/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def mysql_cmd(cls):
        """MySQL mysql Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/mysql'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def mysql_install_db_cmd(cls):
        """MySQL mysql_install_db Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/mysql_install_db'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """MySQL Run Directory
    
        :return: str
        """

        paths = {
            1: '/run/mysqld/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def user_dir(cls):
        """MySQL User Directory
    
        :return: str
        """

        paths = {
            1: '/etc/mysql/users/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def varlib_dir(cls):
        """MySQL Var/Lib Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/mysql/'
        }

        return cls.validate_path(paths.get(cls.value()))
