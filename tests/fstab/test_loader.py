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

MOCK_FILE = MOCK_DATA.joinpath('darwin/fstab')
INVALID_FILE = MOCK_DATA.joinpath('invalid_fstab')

MOCK_INVALID_FILTER_ARG_FIELDS = {
    'uuid': '1234',
    'unexpected': '/'
}
MOCK_INVALID_FILTER_ARG_DATA = {
    'uuid': '',
}
MOCK_VALID_FILTER_ARGS = {
    'uuid': '0FC3B1C4-F072-4A10-A1CE-8ED60A59F03C',
}


def test_fstab_validate_filter_arguments_no_arguments() -> None:
    """
    Test validation of filter arguments with no filter arguments
    """
    with pytest.raises(FilesystemError):
        Fstab().__validate_filter_kwargs__()


def test_fstab_validate_filter_arguments_invalid_fields() -> None:
    """
    Test validation of filter arguments with invalid fields
    """
    with pytest.raises(FilesystemError):
        Fstab().__validate_filter_kwargs__(**MOCK_INVALID_FILTER_ARG_FIELDS)


def test_fstab_validate_filter_arguments_invalid_data() -> None:
    """
    Test validation of filter arguments with invalid data in filters
    """
    with pytest.raises(FilesystemError):
        Fstab().__validate_filter_kwargs__(**MOCK_INVALID_FILTER_ARG_DATA)


def test_fstab_validate_filter_arguments_valid_data() -> None:
    """
    Test validation of filter arguments with invalid data in filters
    """
    kwargs = Fstab().__validate_filter_kwargs__(**MOCK_VALID_FILTER_ARGS)
    assert isinstance(kwargs, dict)
    assert kwargs != {}


# pylint: disable=unused-argument
def test_fstab_unexpeted_platform(unexpected_platform) -> None:
    """
    Test initialzing a Fstab object with unknown platflorm
    """
    with pytest.raises(FilesystemError):
        Fstab()


def test_fstab_get_fstab_lines(monkeypatch) -> None:
    """
    Test calling of the __get_fstab_lines__ internal method to read text line from file
    """
    monkeypatch.setattr('fs_toolkit.fstab.loader.FSTAB_PATH', MOCK_FILE)
    fstab = Fstab()
    assert len(fstab) > 0


def test_fstab_file_read_error(monkeypatch) -> None:
    """
    Test expection raised by the __load_fstab__ method
    """
    monkeypatch.setattr('fs_toolkit.fstab.loader.FSTAB_PATH', INVALID_FILE)
    with pytest.raises(FilesystemError):
        list(Fstab())


def test_fstab_entry_invalid_line(invalid_fstab_line) -> None:
    """
    Test parsing of invalid fstab entry lines
    """
    with pytest.raises(FilesystemError):
        FstabEntry(invalid_fstab_line)


def test_fstab_entry_valid_line(valid_fstab_line) -> None:
    """
    Test parsing of valid fstab entry lines
    """
    obj = FstabEntry(valid_fstab_line)
    assert obj.__line__ == valid_fstab_line
    assert isinstance(hash(obj), int)


def test_fstab_entry_rich_comparison() -> None:
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


def test_get_kwargs_valid(darwin_fstab) -> None:
    """
    Test 'get' with valid value from existing data
    """
    fstab = Fstab()
    item = [entry for entry in fstab if entry.uuid][0]
    assert fstab.get(uuid=item.uuid, mountpoint=item.mountpoint) == item


def test_get_kwargs_conflict(darwin_fstab) -> None:
    """
    Test 'get' with conflict in values for filter fields
    """
    fstab = Fstab()
    item = [entry for entry in fstab if entry.uuid][0]
    other = [entry for entry in fstab if entry != item][0]
    with pytest.raises(FilesystemError):
        fstab.get(uuid=item.uuid, mountpoint=other.mountpoint)


def test_get_kwargs_not_found(darwin_fstab) -> None:
    """
    Test 'get' with valid value from existing data
    """
    assert Fstab().get(uuid=MOCK_VALID_FILTER_ARGS['uuid']) is None


def test_filter_kwargs_not_found(darwin_fstab) -> None:
    """
    Test 'filter' with valid value from existing data
    """
    assert Fstab().filter(uuid=MOCK_VALID_FILTER_ARGS['uuid']) == []


def test_filter_multiple(darwin_fstab) -> None:
    """
    Test 'filter' with arguments that match multiple entries
    """
    fstab = Fstab()
    item = [entry for entry in fstab if entry.uuid][0]
    other = [entry for entry in fstab if entry != item][0]
    assert len(fstab.filter(uuid=item.uuid, mountpoint=other.mountpoint)) == 2
