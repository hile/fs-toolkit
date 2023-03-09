#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.fstab module with macOS Darwin data
"""
from .validators import validate_fstab


def test_darwin_fstab_properties(darwin_fstab):
    """
    Test properties of a macOS darwin fstab object
    """
    validate_fstab(darwin_fstab)

    for entry in darwin_fstab:
        assert isinstance(entry.uuid, str)


def test_darwin_fstab_get_by_uuid(darwin_fstab):
    """
    Get looking up fstab entry by UUID
    """
    item = darwin_fstab[0]
    assert darwin_fstab.get_by_uuid(item.uuid) == item

    assert darwin_fstab.get_by_uuid('abcde') is None
