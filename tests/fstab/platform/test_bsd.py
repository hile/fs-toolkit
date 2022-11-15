"""
Unit tests for fs_toolkit.fstab module with FreeBSD data
"""
from .validators import validate_fstab

BSD_FSTAB_ITEM_COUNT = 2


def test_freebsd_fstab_properties(bsd_fstab):
    """
    Test properties of a BSD fstab object
    """
    validate_fstab(bsd_fstab, BSD_FSTAB_ITEM_COUNT)


def test_freebsd_fstab_get_by_mountpoint(bsd_fstab):
    """
    Test looking up fstab item by mountpoint
    """
    item = bsd_fstab[0]
    assert bsd_fstab.get_by_mountpoint(item.mountpoint) == item
