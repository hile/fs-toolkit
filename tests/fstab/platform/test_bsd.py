#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.fstab module with FreeBSD data
"""
from .validators import validate_fstab


def test_freebsd_fstab_properties(bsd_fstab):
    """
    Test properties of a BSD fstab object
    """
    validate_fstab(bsd_fstab)


def test_freebsd_fstab_get_by_mountpoint(bsd_fstab):
    """
    Test looking up fstab item by mountpoint
    """
    item = bsd_fstab[0]
    assert bsd_fstab.get_by_mountpoint(item.mountpoint) == item
