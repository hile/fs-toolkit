#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common base classes for platform specific mounts classes
"""
from pathlib import Path
from typing import List, Optional, Tuple, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..loader import Mountpoints


# pylint: disable=too-few-public-methods
class MountpointOptions:
    """
    Options for filesystem mount point
    """
    def __init__(self,
                 mountpoint: 'Mountpoint',
                 options: Optional[Union[str, List[str]]]) -> None:
        self.mountpoint = mountpoint
        options = self.__parse_options__(options)
        for flag in options:
            setattr(self, flag, True)

    @staticmethod
    def __parse_options__(options: Union[str, List[str]]) -> List[str]:
        """
        Parse options from string to a list
        """
        if isinstance(options, str):
            options = options.split(', ')
        return options


# pylint: disable=too-few-public-methods
class MountpointUsage:
    """
    Mountpoint usage stats data
    """
    mountpoint: 'Mountpoint'
    size: Optional[int]
    available: Optional[int]
    used: Optional[int]
    percent: Optional[int]

    def __init__(self, mountpoint: 'Mountpoint') -> None:
        self.mountpoint = mountpoint
        self.size = None
        self.available = None
        self.used = None
        self.percent = None

    def __set_value__(self, attr: str, value: int) -> None:
        """
        Set value for usage counter
        """
        value = int(value)
        setattr(self, attr, value)

    def load_data(self, data: dict) -> None:
        """
        Load usage data for mountpoint
        """
        for attr in ('size', 'available', 'used', 'percent'):
            assert attr in data
            self.__set_value__(attr, data[attr])


# pylint: disable=too-few-public-methods
class Filesystem:
    """
    Filesystem for a mountpoint
    """
    mountpoint: 'Mountpoint'
    name: str
    virtual_filesystems: Tuple[str] = ()

    def __init__(self, mountpoint: 'Mountpoint', name: str) -> None:
        self.mountpoint = mountpoint
        self.name = name

    def __repr__(self) -> str:
        return self.name

    @property
    def is_virtual(self) -> bool:
        """
        Return True if filesystem is a virtual filesystem
        """
        return self.name in self.virtual_filesystems


class Mountpoint:
    """
    Filesystem mount point linked to Mountpoints
    """
    mountpoints: 'Mountpoints'
    filesystem_class: Filesystem
    options_class: MountpointOptions
    usage_class: MountpointUsage

    def __init__(self,
                 mountpoints: 'Mountpoints',
                 device: str,
                 mountpoint: str,
                 filesystem: Optional[str] = None,
                 options: Optional[Union[str, List[str]]] = None):
        self.mountpoints = mountpoints
        self.device = device
        self.mountpoint = mountpoint
        self.filesystem = self.filesystem_class(self, filesystem)
        self.options = self.options_class(self, options)
        self.usage = self.usage_class(self)

    def __repr__(self) -> str:
        return f'{self.device} mounted on {self.mountpoint}'

    @property
    def name(self) -> str:
        """
        Return basename of mountpoint as string
        """
        return Path(self.mountpoint).name

    @property
    def is_virtual(self) -> bool:
        """
        Check if filesystem is virtual
        """
        return self.filesystem.is_virtual

    def load_usage_data(self, data: dict) -> None:
        """
        Load filesystem usage data for mountpoint
        """
        self.usage.load_data(data)
