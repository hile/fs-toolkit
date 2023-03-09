#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Validators for fs_toolkit.mounts.platform module
"""
from _collections_abc import list_iterator

import pytest

from fs_toolkit.mounts.loader import Mountpoints, Mountpoint

FILESYSTEMS_NO_USAGE = (
    'autofs',
    'binfmt_misc',
    'bpf',
    'cgroup',
    'cgroup2',
    'configfs',
    'devpts',
    'devtmpfs',
    'efivarfs',
    'fusectl',
    'hugetlbfs',
    'debugfs',
    'mqueue',
    'rpc_pipefs',
    'overlay',
    'ramfs',
    'sysfs',
    'proc',
    'procfs',
    'pstore',
    'securityfs',
    'selinuxfs',
    'tmpfs',
    'tracefs',
    'nsfs',
)


def validate_mountpoint_usage(mountpoint: Mountpoint) -> None:
    """
    Validate a single mountpoint usage parameters are integeres
    """
    for attr in ('size', 'available', 'used', 'percent'):
        value = getattr(mountpoint.usage, attr)
        print(f'mountpoint {mountpoint} filesystem {mountpoint.filesystem} {attr} {value}')
        if mountpoint.filesystem.name not in FILESYSTEMS_NO_USAGE:
            assert isinstance(value, int)


def validate_mountpoint(mountpoint: Mountpoint) -> None:
    """
    Validate a single mountpoint
    """
    assert isinstance(mountpoint.__repr__(), str)
    assert isinstance(mountpoint.name, str)
    assert isinstance(mountpoint.filesystem.__repr__(), str)
    assert isinstance(mountpoint.is_virtual, bool)
    validate_mountpoint_usage(mountpoint)


def validate_mountpoints_properties(
        mountpoints: Mountpoints,
        platform: str,
        toolchain: str) -> None:
    """
    Validate loaded platform specific mountpoint options
    """
    assert mountpoints.__platform__ == platform
    assert mountpoints.__toolchain__ == toolchain

    assert len(mountpoints) > 0
    for mountpoint in mountpoints:
        validate_mountpoint(mountpoint)

    mountpoints.clear()
    with pytest.raises(StopIteration):
        while True:
            mountpoint = next(mountpoints)
            assert isinstance(mountpoint, Mountpoint)

    # Call next() without reloading
    mountpoint = next(mountpoints)
    assert isinstance(mountpoint, Mountpoint)


def validate_mountpoints_iterator(mountpoints: Mountpoints):
    """
    Tests to check mountpoints object iterator action
    """
    assert mountpoints.__loaded__ is None
    iterator = iter(mountpoints)
    assert isinstance(iterator, list_iterator)

    # Returns different instance
    other = iter(mountpoints)
    assert iterator != other
