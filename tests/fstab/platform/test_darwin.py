"""
Unit tests for fs_toolkit.fstab module with macOS Darwin data
"""
from .validators import validate_fstab

DARWIN_FSTAB_ITEM_COUNT = 2


def test_darwin_fstab_properties(darwin_fstab):
    """
    Test properties of a macOS darwin fstab object
    """
    validate_fstab(darwin_fstab, DARWIN_FSTAB_ITEM_COUNT)

    for entry in darwin_fstab:
        assert isinstance(entry.uuid, str)


def test_darwin_fstab_get_by_uuid(darwin_fstab):
    """
    Get looking up fstab entry by UUID
    """
    item = darwin_fstab[0]
    assert darwin_fstab.get_by_uuid(item.uuid) == item

    assert darwin_fstab.get_by_uuid('abcde') is None
