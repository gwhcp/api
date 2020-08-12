import shutil

from worker.queue.os_type import OsType


class SystemPath(OsType):
    def __init__(self):
        super().__init__()

    @classmethod
    def confd_dir(cls):
        """Conf.d Directory
    
        :return: str
        """

        paths = {
            1: '/etc/conf.d/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def echo_cmd(cls):
        """Echo Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/echo'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def grep_cmd(cls):
        """Grep Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/grep'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def group_add_cmd(cls):
        """Group Add Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/groupadd'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def group_del_cmd(cls):
        """Group Delete Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/groupdel'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def initd_dir(cls):
        """System Script Directory
    
        :return: str
        """

        paths = {
            1: '/usr/lib/systemd/system/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ip_base_dir(cls):
        """IP Address Directory
    
        :return: str
        """

        paths = {
            1: '/etc/ipaddress/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def ip_cmd(cls):
        """IP Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/ip'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def kill_cmd(cls):
        """Kill Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/kill'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def log_dir(cls):
        """Log Directory
    
        :return: str
        """

        paths = {
            1: '/var/log/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def mv_cmd(cls):
        """Move Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/mv'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def netctl_base_dir(cls):
        """Netctl Base Directory
    
        :return: str
        """

        paths = {
            1: '/etc/netctl/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def netctl_hooks_dir(cls):
        """Netctl Hooks Directory
    
        :return: str
        """

        return cls.validate_path(f"{cls.netctl_base_dir()}hooks/")

    @classmethod
    def rm_cmd(cls):
        """Remove Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/rm'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def run_dir(cls):
        """Run Directory
    
        :return: str
        """

        paths = {
            1: '/var/run/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def set_quota_cmd(cls):
        """Set Quota Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/setquota'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sh_cmd(cls):
        """Set SH Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/sh'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def su_cmd(cls):
        """SU Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/su'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def sudo_cmd(cls):
        """Sudo Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/sudo'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def systemctl_cmd(cls):
        """SystemCTL Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/systemctl'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def tmpfilesd_dir(cls):
        """Temp Files Directory
    
        :return: str
        """

        paths = {
            1: '/usr/lib/tmpfiles.d/'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def user_add_cmd(cls):
        """User Add Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/useradd'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def user_del_cmd(cls):
        """User Delete Command
    
        :return: str
        """

        paths = {
            1: '/usr/bin/userdel'
        }

        return cls.validate_path(paths.get(cls.value()))

    @classmethod
    def which_cmd(cls, value):
        """Which Command
    
        :param str value: Value
    
        :return: str
        """

        return cls.validate_path(shutil.which(value))
