import os

from django.conf import settings
from rest_framework import serializers


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
            raise serializers.ValidationError(
                'Operating System value cannot return None',
                code='none'
            )

        elif type(settings.OS_TYPE) is not int:
            raise serializers.ValidationError(
                'Operating System value must return an INT',
                code='not_int'
            )

        elif settings.OS_TYPE == 0:
            raise serializers.ValidationError(
                'Operating System value cannot be 0',
                code='zero'
            )

        elif settings.OS_TYPE not in cls.__options():
            raise serializers.ValidationError(
                f'Operating System value cannot exceed {str(len(cls.__options()))}',
                code='not_found'
            )

    @classmethod
    def validate_path(cls, path):
        """Validate Path

        :return: str
        """

        if path is None:
            raise serializers.ValidationError(
                'Path cannot return None',
                code='none'
            )

        elif not os.path.exists(path):
            raise serializers.ValidationError(
                f"Path '{path}' was not found",
                code='not_found'
            )

        return path

    @classmethod
    def value(cls):
        """Returns an Operating System value based on the options above

        :return: int
        """

        # Validate Operating System
        cls.validate_os_type()

        return settings.OS_TYPE
