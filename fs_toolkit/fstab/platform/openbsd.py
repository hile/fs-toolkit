"""
Platform specific code to handle fstab devices on OpenBSD
"""
from pathlib import Path
from typing import Optional

from sys_toolkit.collection import CachedMutableMapping
from sys_toolkit.subprocess import run_command


class DuidMap(CachedMutableMapping):
    """
    OpenBSD Disklabel Unique Identifiers (DUIDs) mapping to device names
    """
    def __get_sysctl_output__(self) -> str:
        """
        Get the sysctl output lines
        """
        stdout, _stderr = run_command(*('sysctl', '-n', 'hw.disknames'))
        return [str(line, 'utf-8') for line in stdout.splitlines()]

    def update(self, other=(), /, **kwds):
        """
        Update DUID map values
        """
        self.__items__ = {}
        self.__start_update__()
        for item in self.__get_sysctl_output__()[0].split(','):
            device, duid = item.split(':', 1)
            if not duid:
                duid = None
            self[device] = duid
        self.__finish_update__()

    def get_device(self, value: str) -> Optional[Path]:
        """
        Get device with full path by DUID. Return None if DUID is not found
        """
        for device, duid in self.items():
            if duid == value:
                return Path(f'/dev/{device}')
        return None
