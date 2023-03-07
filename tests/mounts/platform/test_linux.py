#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.mounts.loader with FreeBSD data
"""
from .validators import (
    validate_mountpoints_properties,
    validate_mountpoints_iterator,
)

LINUX_MOUNT_POINT_COUNT = 42


def test_linux_mountpoints(linux_mountpoints):
    """
    Test loading Linux mountpoints data
    """
    validate_mountpoints_properties(linux_mountpoints, LINUX_MOUNT_POINT_COUNT, 'linux', 'gnu')


def test_linux_mountpoints_iterator(linux_mountpoints):
    """
    Test initializing an iterator from mountpoints
    """
    validate_mountpoints_iterator(linux_mountpoints)
