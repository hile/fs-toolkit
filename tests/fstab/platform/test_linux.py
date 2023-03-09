#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.fstab module with Linux data
"""
from .validators import validate_fstab

# Trivial cases, the linux way with spaces and tabs in mountpoint
FSTAB_SPACED_MOUNTPOINT = '/dir with spaces'
FSTAB_TABBED_MOUNTPOINT = '/dir\twith\ttabs'


def test_linux_fstab_properties(linux_fstab):
    """
    Test properties of a Linux fstab object
    """
    for item in linux_fstab:
        print(item)
    validate_fstab(linux_fstab)


def test_linux_fstab_get_by_device(linux_fstab):
    """
    Get looking up fstab entry by label
    """
    for item in linux_fstab:
        if item.device is not None:
            print(f'look up device {item.device}')
            assert linux_fstab.get_by_device(item.device) == item


def test_linux_fstab_get_by_label(linux_fstab):
    """
    Get looking up fstab entry by label
    """
    item = linux_fstab[0]
    assert linux_fstab.get_by_label(item.label) == item
    assert linux_fstab.get_by_label('abcde') is None


def test_linux_fstab_get_by_mountpoint_encoded(fstab_encoded_paths):
    """
    Get looking up fstab entry by mountpoint with encoded filenames
    """
    assert len(fstab_encoded_paths) == 2
    spaced = fstab_encoded_paths[0]
    tabbed = fstab_encoded_paths[1]
    for item in fstab_encoded_paths:
        print(f'{item} {item.mountpoint}')
    item = fstab_encoded_paths.get_by_mountpoint(FSTAB_SPACED_MOUNTPOINT)
    assert item is not None
    assert item == spaced
    item = fstab_encoded_paths.get_by_mountpoint(FSTAB_TABBED_MOUNTPOINT)
    assert item is not None
    assert item == tabbed
