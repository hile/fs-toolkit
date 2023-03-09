#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Mountpoints loader main class MountPoints()
"""
from re import Pattern
from typing import List, Optional, Tuple

from sys_toolkit.subprocess import run_command

from ..base import LineLoader
from ..exceptions import FilesystemError
from .platform.base import Mountpoint
from .platform.bsd import BSDMountpoint
from .platform.darwin import DarwinMountPoint
from .platform.linux import LinuxMountPoint
from .platform.openbsd import OpenBSDMountPoint


from .constants import (
    GNU_MOUNT_COMMAND,
    GNU_DF_COMMAND,
    BSD_MOUNT_COMMAND,
    BSD_DF_COMMAND,
    RE_GNU_MOUNT_LINE,
    RE_GNU_DF_LINE,
    RE_BSD_MOUNT_LINE,
    RE_BSD_DF_LINE,
)


class Mountpoints(LineLoader):
    """
    Filesystem mount points with usage
    """
    __mountpoint_class__: Mountpoint
    __mount_command__: Tuple[str] = None
    __df_command__: Tuple[str] = None
    __re_mount_patterns__: Optional[List[Pattern]] = None
    __re_df_patterns__: Optional[List[Pattern]] = None

    def __init__(self):
        super().__init__()
        self.__detect_mountpoint_class__()
        self.__initialize_toolchain_based_data__()
        self.__iter_items__ = None

    def __detect_mountpoint_class__(self) -> None:
        """
        Detect mountpoint loader class based on platform family
        """
        if self.__platform__ == 'bsd':
            self.__mountpoint_class__ = BSDMountpoint
        elif self.__platform__ == 'darwin':
            self.__mountpoint_class__ = DarwinMountPoint
        elif self.__platform__ == 'linux':
            self.__mountpoint_class__ = LinuxMountPoint
        elif self.__platform__ == 'openbsd':
            self.__mountpoint_class__ = OpenBSDMountPoint
        else:
            raise FilesystemError(f'Unsupported OS platform: {self.__platform__}')

    def __initialize_toolchain_based_data__(self) -> None:
        """
        Initialize toolchain specific commands and regexp patterns
        """
        if self.__toolchain__ == 'bsd':
            self.__mount_command__ = BSD_MOUNT_COMMAND
            self.__df_command__ = BSD_DF_COMMAND
            self.__re_mount_patterns__ = RE_BSD_MOUNT_LINE
            self.__re_df_patterns__ = RE_BSD_DF_LINE

        elif self.__toolchain__ in ('gnu', 'openbsd'):
            self.__mount_command__ = GNU_MOUNT_COMMAND
            self.__df_command__ = GNU_DF_COMMAND
            self.__re_mount_patterns__ = RE_GNU_MOUNT_LINE
            self.__re_df_patterns__ = RE_GNU_DF_LINE

        else:
            raise FilesystemError(f'Unexpected toolchain detected: {self.__toolchain__}')

    def __get_mount_lines__(self) -> List[str]:
        """
        Return lines from mount command
        """
        stdout, _stderr = run_command(*self.__mount_command__)
        return [str(line, 'utf-8') for line in stdout.splitlines()]

    def __get_df_lines__(self) -> List[str]:
        """
        Return lines from df command
        """
        stdout, _stderr = run_command(*self.__df_command__)
        return [str(line, 'utf-8') for line in stdout.splitlines()]

    def __get_mountpoint_data__(self, lines: List[str]) -> List[dict]:
        """
        Return lines from mount command
        """
        return self.__match_pattern_list__(lines, self.__re_mount_patterns__)

    def __get_df_data__(self, lines: List[str]) -> List[dict]:
        """
        Return lines from df command
        """
        return self.__match_pattern_list__(lines, self.__re_df_patterns__)

    def append(self, value: Mountpoint) -> Mountpoint:
        assert isinstance(value, Mountpoint)
        return super().append(value)

    def insert(self, index: int, value: Mountpoint) -> Mountpoint:
        assert isinstance(value, Mountpoint)
        return super().insert(index, value)

    def update(self) -> None:
        """
        Get data for mountpoints
        """
        self.clear()
        self.__start_update__()
        mountpoints = {}
        for match in self.__get_mountpoint_data__(self.__get_mount_lines__()):
            item = self.__mountpoint_class__(self, **match)
            mountpoints[item.mountpoint] = item
            self.append(item)

        for match in self.__get_df_data__(self.__get_df_lines__()):
            item = mountpoints.get(match['mountpoint'], None)
            if item is not None:
                item.load_usage_data(match)
        self.__finish_update__()
