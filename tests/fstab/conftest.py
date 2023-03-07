#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit test configuration for fs_toolkit.fstab module
"""
import pytest

INVALID_FSTAB_ENTRIES = (
    '',
    'foo bar baz',
)
VALID_FSTAB_ENTRIES = (
    '8FEC6205A1D4449C.k /usr/obj ffs rw,nodev,nosuid 1 2',
    'UUID=901C5425-95A6-4735-975D-0FE7D1AC76A9 /Users/pytest/Documents/Private apfs rw,nosuid,nodev',
)


@pytest.fixture(params=INVALID_FSTAB_ENTRIES)
def invalid_fstab_line(request):
    """
    Fixture with invalid fstab entry lines
    """
    yield request.param


@pytest.fixture(params=VALID_FSTAB_ENTRIES)
def valid_fstab_line(request):
    """
    Fixture with valid fstab entry lines
    """
    yield request.param
