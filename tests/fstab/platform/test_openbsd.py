#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for fs_toolkit.fstab.platform.openbsd module
"""
from pathlib import Path

from sys_toolkit.tests.mock import MockRun

from fs_toolkit.fstab.platform.openbsd import DuidMap

from ...conftest import MOCK_DATA
from .validators import validate_fstab

MOCK_DUID_DATA = MOCK_DATA.joinpath('openbsd/sysctl.hw.disknames')

OPENBSD_FSTAB_ITEM_COUNT = 10

MOCK_DUID_MAP_ITEM_COUNT = 3
INVALID_DUID = '12345567812345678'
VALID_DUID = '149427019F845CBB'
VALID_DUID_DEVICE = Path('/dev/sd1')


# pylint:disable=too-few-public-methods
class MockRunDuiDCommands(MockRun):
    """
    Mock calls to collect data from DUID map sysctl
    """
    def __init__(self, stderr: str = '') -> None:
        super().__init__(encoding='utf-8')
        self.stderr = stderr
        self.duid_data = MOCK_DUID_DATA.read_bytes()

    def __call__(self, *args, **kwargs):
        """
        Call mocked check_output, storing call argument and returning data
        """
        super().__call__(*args, **kwargs)
        if args[0] == 'sysctl':
            return self.duid_data, self.stderr
        raise ValueError(f'Unexpected command arguments: {args}')


# pylint: disable=unused-argument
def test_load_duidmap__get_sysctl_output__(monkeypatch):
    """
    Mock the __get_sysctl_output__ return value for DUID map, loading 'real' data
    with 'real' commmand
    """
    mock_method = MockRunDuiDCommands()
    monkeypatch.setattr('fs_toolkit.fstab.platform.openbsd.run_command', mock_method)
    obj = DuidMap()
    assert len(obj.keys()) == MOCK_DUID_MAP_ITEM_COUNT


# pylint: disable=unused-argument
def test_load_duidmap(openbsd_fstab):
    """
    Test loading OpenBSD DUID map with mocked sysctl data
    """
    obj = DuidMap()
    assert len(obj.keys()) == MOCK_DUID_MAP_ITEM_COUNT


# pylint: disable=unused-argument
def test_load_duidmap_get_device_valid(openbsd_fstab):
    """
    Test looking up a valid device from OpenBSD DUID map
    """
    obj = DuidMap()
    assert obj.get_device(VALID_DUID) == VALID_DUID_DEVICE


def test_load_duidmap_get_device_invalid(openbsd_fstab):
    """
    Test looking up a invalid device from OpenBSD DUID map
    """
    obj = DuidMap()
    assert obj.get_device(INVALID_DUID) is None


def test_openbsd_fstab_properties(openbsd_fstab):
    """
    Test properties of a OpenBSD fstab object
    """
    validate_fstab(openbsd_fstab, OPENBSD_FSTAB_ITEM_COUNT)
