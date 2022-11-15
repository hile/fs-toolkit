"""
Loader for fstab file details with OS specific
"""
from pathlib import Path
from operator import eq, ne, ge, gt, le, lt
from typing import List, Optional

from ..base import LineLoader
from ..exceptions import FilesystemError
from .constants import FSTAB_PATH, FSTAB_FIELDS, FSTAB_INT_FIELDS, FSTAB_FILE_NONE_VALUES


class FstabItem:
    """
    Generic fstab item text line
    """
    __line__: str

    def __init__(self, line: str) -> None:
        self.__line__ = line

    def __repr__(self) -> str:
        return str(self.__line__)

    def __compare__(self, other, operator):
        """
        Compare fstab items to string or FstabItem
        """
        if isinstance(other, str):
            return operator(self.__line__, other)
        if isinstance(other, FstabItem):
            return operator(self.__line__, other.__line__)
        raise TypeError(f'Error comparing FstabItem to {type(other)}: unexpected object')

    def __eq__(self, other):
        return self.__compare__(other, eq)

    def __ne__(self, other):
        return self.__compare__(other, ne)

    def __ge__(self, other):
        return self.__compare__(other, ge)

    def __gt__(self, other):
        return self.__compare__(other, gt)

    def __le__(self, other):
        return self.__compare__(other, le)

    def __lt__(self, other):
        return self.__compare__(other, lt)


# pylint: disable=too-few-public-methods
class FstabComment(FstabItem):
    """
    Comment line in fstab
    """


class FstabEntry(FstabItem):
    """
    Line in fstab
    """
    fs_spec: str
    fs_file: str
    fs_vfstype: str
    fs_mntops: str
    fs_freq: Optional[int]
    fs_freq: Optional[int]

    def __init__(self, line: str) -> None:
        super().__init__(line)
        self.__parse_line__(line)

    def __parse_line__(self, line: str) -> None:
        """
        Parse fstab line to entry attributes with FSTAB_FIELDS
        """
        fields = line.split()
        if len(fields) < 4 or len(fields) > 6:
            raise FilesystemError(f'Invalid fstab line: {line}')
        for index, field in enumerate(FSTAB_FIELDS):
            try:
                value = fields[index]
            except IndexError:
                value = None
            if field in FSTAB_INT_FIELDS and value is not None:
                value = int(value)
            setattr(self, field, value)

    @property
    def device(self) -> Optional[Path]:
        """
        Return path of device if fs_spec contains a path
        """
        return Path(self.fs_spec) if self.fs_spec[0] == '/' else None

    @property
    def label(self) -> Optional[str]:
        """
        Return label of device if fs_spec is in LABEL format
        """
        return self.fs_spec[5:] if self.fs_spec[:5].upper() == 'LABEL=' else None

    @property
    def mountpoint(self) -> Optional[Path]:
        """
        Return path of device if fs_spec contains a path
        """
        return Path(self.fs_file) if self.fs_file not in FSTAB_FILE_NONE_VALUES else None

    @property
    def options(self) -> List[str]:
        """
        Return filesystem options as list of strings
        """
        return self.fs_mntops.split(',')

    @property
    def partition_label(self) -> Optional[str]:
        """
        Return partition LABEL of device if fs_spec is in PARTLABEL format
        """
        return self.fs_spec[10:] if self.fs_spec[:10].upper() == 'PARTLABEL=' else None

    @property
    def partition_uuid(self) -> Optional[str]:
        """
        Return partition UUID of device if fs_spec is in PARTUUID format
        """
        return self.fs_spec[9:] if self.fs_spec[:9].upper() == 'PARTUUID=' else None

    @property
    def uuid(self) -> Optional[str]:
        """
        Return UUID of device if fs_spec is in UUID format
        """
        return self.fs_spec[5:] if self.fs_spec[:5].upper() == 'UUID=' else None

    @property
    def vfstypes(self) -> List[str]:
        """
        Return filesystem types as list of strings
        """
        return self.fs_vfstype.split(',')


class Fstab(LineLoader):
    """
    Lines in /etc/fstab
    """
    __lines__: list[str]

    def __init__(self, path: Optional[str] = None) -> None:
        super().__init__()
        self.path = Path(path) if path is not None else FSTAB_PATH
        self.__lines__ = []

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
                self.__lines__.append(FstabComment(line))
                continue

            entry = FstabEntry(line)
            self.__lines__.append(entry)
            self.append(entry)

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

    def __encode_mountpoint_path__(self, path: str) -> Path:
        """
        Encode mountpoint path string. Replaces space and tab in string with
        escape sequences ’\040' and '\011' respectively as is done on Linux

        For full BSD compatibility this should implement full strunvis(3) encoding support
        """
        return Path(str(path).replace(' ', '\\040').replace('\t', '\\011'))

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
