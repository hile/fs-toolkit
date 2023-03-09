#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.fstab.loader module
"""
import pytest

from fs_toolkit.exceptions import FilesystemError
from fs_toolkit.fstab.loader import Fstab, FstabEntry

from ..conftest import MOCK_DATA
from .conftest import VALID_FSTAB_ENTRIES
from .platform.test_darwin import DARWIN_FSTAB_ITEM_COUNT

MOCK_FILE = MOCK_DATA.joinpath('darwin/fstab')
INVALID_FILE = MOCK_DATA.joinpath('invalid_fstab')


# pylint: disable=unused-argument
def test_fstab_unexpeted_platform(unexpected_platform) -> None:
    """
    Test initialzing a Fstab object with unknown platflorm
    """
    with pytest.raises(FilesystemError):
        Fstab()


def test_fstab_get_fstab_lines(monkeypatch):
    """
    Test calling of the __get_fstab_lines__ internal method to read text line from file
    """
    monkeypatch.setattr('fs_toolkit.fstab.loader.FSTAB_PATH', MOCK_FILE)
    fstab = Fstab()
    assert len(fstab) == DARWIN_FSTAB_ITEM_COUNT


def test_fstab_file_read_error(monkeypatch):
    """
    Test expection raised by the __load_fstab__ method
    """
    monkeypatch.setattr('fs_toolkit.fstab.loader.FSTAB_PATH', INVALID_FILE)
    with pytest.raises(FilesystemError):
        list(Fstab())


def test_fstab_entry_invalid_line(invalid_fstab_line):
    """
    Test parsing of invalid fstab entry lines
    """
    with pytest.raises(FilesystemError):
        FstabEntry(invalid_fstab_line)


def test_fstab_entry_valid_line(valid_fstab_line):
    """
    Test parsing of valid fstab entry lines
    """
    obj = FstabEntry(valid_fstab_line)
    assert obj.__line__ == valid_fstab_line


def test_fstab_entry_rich_comparison():
    """
    Test rich comparison methods of fstab entries
    """
    a = FstabEntry(VALID_FSTAB_ENTRIES[0])
    b = FstabEntry(VALID_FSTAB_ENTRIES[1])

    assert not a == b  # pylint: disable=unneeded-not
    assert a != b
    assert a < b
    assert a <= b
    assert b > a
    assert b >= a

    assert not a == str(b)  # pylint: disable=unneeded-not
    assert a != str(b)
    assert a < str(b)
    assert a <= str(b)
    assert b > str(a)
    assert b >= str(a)

    with pytest.raises(TypeError):
        assert a == 0
    with pytest.raises(TypeError):
        assert a != 0
    with pytest.raises(TypeError):
        assert a < 0
    with pytest.raises(TypeError):
        assert a > 0
    with pytest.raises(TypeError):
        assert a <= 0
    with pytest.raises(TypeError):
        assert a >= 0
