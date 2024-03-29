#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Generic BSD mountpoints (FreeBSD, MacOS)
"""
from typing import List, Optional, Union
from .base import Mountpoint, Filesystem, MountpointOptions, MountpointUsage

BSD_VIRTUAL_FILESYSTEMS = (
    'devfs',
    'procfs',
)


# pylint: disable=too-few-public-methods
class BSDMountpointUsage(MountpointUsage):
    """
    BSD specific mountpoint usage data
    """
    inodes_used: Optional[int]
    inodes_available: Optional[int]
    inodes_percent: Optional[int]

    def __init__(self, mountpoint: 'BSDMountpoint') -> None:
        super().__init__(mountpoint)
        self.inodes_used = None
        self.inodes_available = None
        self.inodes_percent = None

    def load_data(self, data: dict) -> None:
        """
        Load BSD specific filesystem usage data
        """
        super().load_data(data)
        for attr in ('inodes_used', 'inodes_available', 'inodes_percent'):
            if attr in data:
                self.__set_value__(attr, data[attr])


# pylint: disable=too-few-public-methods
class BSDMountPointOptions(MountpointOptions):
    """
    BSD specific mountpoint options
    """
    def __init__(self,
                 mountpoint: 'BSDMountpoint',
                 options: Optional[Union[str, List[str]]] = None) -> None:
        options = self.__parse_options__(options)
        filesystem = options[0]
        options = options[1:]

        super().__init__(mountpoint, options)
        self.mountpoint.filesystem.name = filesystem


# pylint: disable=too-few-public-methods
class BSDFilesystem(Filesystem):
    """
    BSD specific mountpoint filesystem

    On BSD systems filesystem name comes from options
    """
    virtual_filesystems = BSD_VIRTUAL_FILESYSTEMS


class BSDMountpoint(Mountpoint):
    """
    BSD specific mountpoint
    """
    filesystem_class = BSDFilesystem
    options_class = BSDMountPointOptions
    usage_class = BSDMountpointUsage
