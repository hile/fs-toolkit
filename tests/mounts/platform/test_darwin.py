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


def test_darwin_mountpoints(darwin_mountpoints):
    """
    Test loading macOS darwin mountpoints data
    """
    validate_mountpoints_properties(darwin_mountpoints, 'darwin', 'bsd')


def test_darwin_mountpoints_iterator(darwin_mountpoints):
    """
    Test initializing an iterator from mountpoints
    """
    validate_mountpoints_iterator(darwin_mountpoints)
