"""
Unit tests for fs_toolkit.mounts.loader with FreeBSD data
"""
from .validators import (
    validate_mountpoints_properties,
    validate_mountpoints_iterator,
)

OPENBSD_MOUNT_POINT_COUNT = 3


# pylint: disable=unused-argument
def test_openbsd_mountpoints(openbsd_mountpoints):
    """
    Test loading OpenBSD mountpoints data
    """
    validate_mountpoints_properties(openbsd_mountpoints, OPENBSD_MOUNT_POINT_COUNT, 'openbsd', 'openbsd')


def test_openbsd_mountpoints_iterator(openbsd_mountpoints):
    """
    Test initializing an iterator from mountpoints
    """
    validate_mountpoints_iterator(openbsd_mountpoints)
