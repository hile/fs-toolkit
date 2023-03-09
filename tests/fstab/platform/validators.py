#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Validators for fs_toolkit.mounts.fstab module
"""
from pathlib import Path
from typing import List, Optional

from fs_toolkit.fstab.loader import Fstab, FstabEntry

FSTAB_ENTRY_PATH_ATTRIBUTES = (
    'device',
    'mountpoint',
)
FSTAB_ENTRY_STRING_ATTRIBUTES = (
    'uuid',
    'label',
    'partition_label',
    'partition_uuid',
)
FSTAB_ENTRY_STRING_LIST_ATTRIBUTES = (
    'options',
    'vfstypes',
)


def validate_optional_path_attribute(attribute: Optional[str]) -> None:
    """
    Validate an attribute is Path or None
    """
    if attribute is not None:
        assert isinstance(attribute, Path)


def validate_optional_string_attribute(attribute: Optional[str]) -> None:
    """
    Validate an attribute is a non-empty string or None
    """
    if attribute is not None:
        assert isinstance(attribute, str)
        assert attribute != ''


def validate_string_list_attribute(attribute: List[str]) -> None:
    """
    Validate attribute is a list of strings
    """
    assert isinstance(attribute, list)
    for item in attribute:
        assert isinstance(item, str)


def validate_fstab_entry(entry: FstabEntry) -> None:
    """
    Test fstab entry object
    """
    assert isinstance(entry.__repr__(), str)

    for attr in FSTAB_ENTRY_PATH_ATTRIBUTES:
        validate_optional_path_attribute(getattr(entry, attr))

    for attr in FSTAB_ENTRY_STRING_ATTRIBUTES:
        validate_optional_string_attribute(getattr(entry, attr))

    for attr in FSTAB_ENTRY_STRING_LIST_ATTRIBUTES:
        validate_string_list_attribute(getattr(entry, attr))


def validate_fstab(fstab: Fstab) -> None:
    """
    Test fstab object
    """
    print(f'{fstab.__platform__} total {len(fstab)}')
    assert isinstance(fstab, Fstab)
    assert isinstance(fstab.__repr__(), str)

    assert len(fstab) > 0
    for entry in fstab:
        validate_fstab_entry(entry)
