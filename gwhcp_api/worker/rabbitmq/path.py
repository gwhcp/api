from worker.queue.os_type import OsType


class RabbitmqPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def conf_dir(cls):
        """RabbitMQ Configuration Directory
    
        :return: str
        """

        paths = {
            1: '/etc/rabbitmq/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def home_dir(cls):
        """RabbitMQ Home Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/rabbitmq/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """RabbitMQ Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/rabbitmq/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def mnesia_dir(cls):
        """RabbitMQ Mnesia Directory
    
        :return: str
        """

        paths = {
            1: '/var/lib/rabbitmq/mnesia/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def rabbitmqctl_cmd(cls):
        """RabbitMQ rabbitmqctl Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/rabbitmqctl'
        }

        return cls.validate_path(paths.get(cls.value()))
