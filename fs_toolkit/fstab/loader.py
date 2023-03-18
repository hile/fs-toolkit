#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Loader for fstab file details with OS specific
"""
from pathlib import Path
from typing import Dict, List, Optional

from ..base import LineLoader
from ..exceptions import FilesystemError
from .constants import FSTAB_PATH

from .platform.base import FstabComment, FstabEntry
from .platform.bsd import BSDFstabComment, BSDFstabEntry
from .platform.darwin import DarwinFstabComment, DarwinFstabEntry
from .platform.linux import LinuxFstabComment, LinuxFstabEntry
from .platform.openbsd import OpenBSDFstabComment, OpenBSDFstabEntry

FILTER_ARGS = (
    'device',
    'label',
    'mountpoint',
    'uuid'
)


class Fstab(LineLoader):
    """
    Lines in /etc/fstab
    """
    path: Path
    __fstab_entry_class__: FstabEntry
    __fstab_comment_class__: FstabComment
    __lines__: list[str]

    def __init__(self, path: Optional[str] = None) -> None:
        super().__init__()
        self.__detect_fstab_class__()
        self.path = Path(path) if path is not None else FSTAB_PATH
        self.__lines__ = []

    def __detect_fstab_class__(self) -> None:
        """
        Detect platform specific class for fstab items
        """
        if self.__platform__ == 'bsd':
            self.__fstab_entry_class__ = BSDFstabEntry
            self.__fstab_comment_class__ = BSDFstabComment
        elif self.__platform__ == 'darwin':
            self.__fstab_entry_class__ = DarwinFstabEntry
            self.__fstab_comment_class__ = DarwinFstabComment
        elif self.__platform__ == 'linux':
            self.__fstab_entry_class__ = LinuxFstabEntry
            self.__fstab_comment_class__ = LinuxFstabComment
        elif self.__platform__ == 'openbsd':
            self.__fstab_entry_class__ = OpenBSDFstabEntry
            self.__fstab_comment_class__ = OpenBSDFstabComment
        else:
            raise FilesystemError(f'Unsupported OS platform: {self.__platform__}')

    def __get_fstab_lines__(self) -> List[str]:
        """
        Load lines from fstab file as unicode strings
        """
        with self.path.open('r', encoding='utf-8') as handle:
            return handle.readlines()

    def __load_fstab__(self) -> None:
        """
        Load fstab lines. This is called from update() method only
        """
        self.__lines__ = []
        for line in self.__get_fstab_lines__():
            line = line.rstrip()
            if line == '' or line.startswith('#'):
                self.__lines__.append(self.__fstab_comment_class__(line))
                continue

            entry = self.__fstab_entry_class__(line)
            self.__lines__.append(entry)
            self.append(entry)

    def __encode_mountpoint_path__(self, path: str) -> Path:
        """
        Encode mountpoint path string. Replaces space and tab in string with
        escape sequences ’\040' and '\011' respectively as is done on Linux

        For full BSD compatibility this should implement full strunvis(3) encoding support
        """
        return Path(str(path).replace(' ', '\\040').replace('\t', '\\011')).expanduser()

    def __get_by_attr__(self, attr: str, value: str) -> Optional[FstabEntry]:
        """
        Get an entry by property or attribute value. Returns None if no match is found
        """
        for item in self:
            if getattr(item, attr, None) == value:
                return item
        return None

    def get_by_uuid(self, uuid: str) -> Optional[FstabEntry]:
        """
        Get a fstab item by UUID
        """
        return self.__get_by_attr__('uuid', uuid)

    def get_by_label(self, label: str) -> Optional[FstabEntry]:
        """
        Get a fstab item by label
        """
        return self.__get_by_attr__('label', label)

    def get_by_device(self, path: str) -> Optional[FstabEntry]:
        """
        Get a fstab item by label
        """
        return self.__get_by_attr__('device', Path(path))

    def get_by_mountpoint(self, path: str) -> Optional[FstabEntry]:
        """
        Get a fstab item by label
        """
        return self.__get_by_attr__('mountpoint', self.__encode_mountpoint_path__(path))

    def __validate_filter_kwargs__(self, **kwargs: Dict[str, str]) -> Dict[str, str]:
        """
        Validate kwargs used for filtering
        """
        if not kwargs:
            raise FilesystemError('Missing filter arguments')
        if not set(kwargs.keys()).issubset(set(FILTER_ARGS)):
            raise FilesystemError('Invalid query arguments')
        for attr, value in kwargs.items():
            if not value:
                raise FilesystemError(f'Empty value for {attr} filter')
        return kwargs

    def get(self, **kwargs: Dict[str, str]) -> Optional[FstabEntry]:
        """
        Unified 'get' function to fetch item by one or more specified attributes

        Valid fields for kwargs are 'device', label', 'mountpoint' and 'uuid'
        """
        entry = None
        for attr, value in self.__validate_filter_kwargs__(**kwargs).items():
            match = getattr(self, f'get_by_{attr}')(value)
            if match:
                if entry and match != entry:
                    raise FilesystemError('Query arguments match different fstab enties')
                entry = match
        return entry

    def filter(self, **kwargs: Dict[str, str]) -> List[FstabEntry]:
        """
        Similar to 'get' method but can return multiple different fstab entries
        matching filter arguments
        """
        matches = []
        for attr, value in self.__validate_filter_kwargs__(**kwargs).items():
            match = getattr(self, f'get_by_{attr}')(value)
            if match:
                matches.append(match)
        return matches

    def update(self) -> None:
        """
        Update fstab information
        """
        self.clear()
        self.__start_update__()
        try:
            self.__load_fstab__()
        except FilesystemError as error:
            self.__reset__()
            raise FilesystemError(error) from error
        self.__finish_update__()
