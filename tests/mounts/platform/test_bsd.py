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

FREEBSD_MOUNT_POINT_COUNT = 13


def test_freebsd_mountpoints(bsd_mountpoints):
    """
    Test loading FreeBSD mountpoints data
    """
    validate_mountpoints_properties(bsd_mountpoints, FREEBSD_MOUNT_POINT_COUNT, 'bsd', 'bsd')


def test_freebsd_mountpoints_iterator(bsd_mountpoints):
    """
    Test initializing an iterator from mountpoints
    """
    validate_mountpoints_iterator(bsd_mountpoints)
