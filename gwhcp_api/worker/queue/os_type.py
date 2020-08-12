import os

from django.conf import settings


class OsType:
    @staticmethod
    def __options():
        """Valid Operating Systems

        :return: dict
        """

        return {
            1: 'Archlinux',
            2: 'Ubuntu',
            3: 'FreeBSD'
        }

    @classmethod
    def validate_os_type(cls):
        """Validate Operating System

        :return: None
        """

        if settings.OS_TYPE is None:
            raise ValueError('Operating System value cannot return None')

        elif type(settings.OS_TYPE) is not int:
            raise ValueError('Operating System value must return an INT')

        elif settings.OS_TYPE == 0:
            raise ValueError('Operating System value cannot be 0')

        elif settings.OS_TYPE not in cls.__options():
            raise ValueError(f'Operating System value cannot exceed {str(len(cls.__options()))}')

    @classmethod
    def validate_path(cls, path):
        """Validate Path

        :return: str
        """

        if path is None:
            raise KeyError('Path cannot return None')

        elif not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' was not found")

        return path

    @classmethod
    def value(cls):
        """Returns an Operating System value based on the options above

        :return: int
        """

        # Validate Operating System
        cls.validate_os_type()

        return settings.OS_TYPE
