#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests configuration for fs_toolkit module
"""
from pathlib import Path
from typing import Any, Dict, Iterator, List, Union

import pytest

from sys_toolkit.tests.mock import MockCalledMethod

from fs_toolkit.fstab import Fstab
from fs_toolkit.mounts import Mountpoints

MOCK_DATA = Path(__file__).parent.joinpath('mock')

PLATFORM_MAP = {
    'freebsd': 'bsd',
}
TOOLCHAIN_MAP = {
    'freebsd': 'bsd',
    'darwin': 'bsd',
    'linux': 'gnu',
    'openbsd': 'openbsd',
}

MOCK_DATA_VARIANTS_BSD = (
    'freebsd13',
)
MOCK_VARIANTS_DARWIN = (
    'darwin',
)
MOCK_VARIANTS_LINUX = (
    'almalinux9',
    'debian-bullseye',
    'devuan-chimaera',
    'linux',
    'opensuse-leap',
    'rockylinux9',
    'ubuntu-jammy',
)
MOCK_VARIANTS_OPENBSD = (
    'openbsd7',
)

UNEXPECTED_PLATFORM = 'windows'
UNEXPECTED_TOOLCHAIN = 'other'


# pylint: disable=too-few-public-methods
class LoadMockData(MockCalledMethod):
    """
    Load mock data as text lines
    """
    platform: str
    filename: Union[str, Path]

    def __init__(self, platform: str, filename: Union[str, Path]) -> None:
        super().__init__()
        self.platform = platform
        self.filename = filename

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> List[str]:
        """
        Return mocked data as text lines
        """
        super().__init__(*args, **kwargs)
        with MOCK_DATA.joinpath(self.filename).open('r', encoding='utf-8') as handle:
            return handle.readlines()


def mock_openbsd_duidmap(monkeypatch):
    """
    Mock reading of the OpenBSD DUID map sysctl
    """
    monkeypatch.setattr(
        'fs_toolkit.fstab.platform.openbsd.DuidMap.__get_sysctl_output__',
        LoadMockData('openbsd', 'openbsd7/sysctl.hw.disknames')
    )


def mock_platform_toolchain(monkeypatch, environment: str) -> None:
    """
    Mock platform and toolchain
    """
    monkeypatch.setattr(
        'fs_toolkit.base.detect_platform_family',
        MockCalledMethod(return_value=PLATFORM_MAP.get(environment, environment))
    )
    monkeypatch.setattr(
        'fs_toolkit.base.detect_toolchain_family',
        MockCalledMethod(return_value=TOOLCHAIN_MAP.get(environment, environment))
    )


def mock_data_loaders(monkeypatch, platform: str, environment: str) -> None:
    """
    Mock mount and df command data outputs
    """
    monkeypatch.setattr(
        'fs_toolkit.fstab.loader.Fstab.__get_fstab_lines__',
        LoadMockData(platform, f'{environment}/fstab')
    )
    monkeypatch.setattr(
        'fs_toolkit.mounts.loader.Mountpoints.__get_mount_lines__',
        LoadMockData(platform, f'{environment}/mount')
    )
    monkeypatch.setattr(
        'fs_toolkit.mounts.loader.Mountpoints.__get_df_lines__',
        LoadMockData(platform, f'{environment}/df')
    )


def mock_environment_fstab(monkeypatch, platform: str, environment: str) -> Fstab:
    """
    Mock specified platform, toolchain and data for Fstab class
    """
    mock_platform_toolchain(monkeypatch, platform)
    mock_data_loaders(monkeypatch, platform, environment)
    return Fstab()


def mock_environment_mountpoints(monkeypatch, platform: str, environment: str) -> Mountpoints:
    """
    Mock specified platform, toolchain and data for Mountpoints class
    """
    mock_platform_toolchain(monkeypatch, platform)
    mock_data_loaders(monkeypatch, platform, environment)
    return Mountpoints()


@pytest.fixture
def mock_platform_data(monkeypatch) -> Iterator[Mountpoints]:
    """
    Mock platform and toolchain without data
    """
    mock_platform_toolchain(monkeypatch, 'freebsd')
    yield Mountpoints()


@pytest.fixture(params=MOCK_DATA_VARIANTS_BSD)
def bsd_fstab(monkeypatch, request) -> Iterator[Fstab]:
    """
    Mock loading of BSD fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'freebsd', request.param)


@pytest.fixture(params=MOCK_DATA_VARIANTS_BSD)
def bsd_mountpoints(monkeypatch, request) -> Iterator[Mountpoints]:
    """
    Mock loading of BSD mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'freebsd', request.param)


@pytest.fixture(params=MOCK_VARIANTS_DARWIN)
def darwin_fstab(monkeypatch, request) -> Iterator[Fstab]:
    """
    Mock loading of macOS darwin fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'darwin', request.param)


@pytest.fixture(params=MOCK_VARIANTS_DARWIN)
def darwin_mountpoints(monkeypatch, request) -> Iterator[Mountpoints]:
    """
    Mock loading of macOS darwin mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'darwin', request.param)


@pytest.fixture(params=MOCK_VARIANTS_LINUX)
def linux_fstab(monkeypatch, request) -> Iterator[Fstab]:
    """
    Mock loading of Linux fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'linux', request.param)


@pytest.fixture(params=MOCK_VARIANTS_LINUX)
def linux_mountpoints(monkeypatch, request) -> Iterator[Mountpoints]:
    """
    Mock loading of Linux mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'linux', request.param)


@pytest.fixture(params=MOCK_VARIANTS_OPENBSD)
def openbsd_fstab(monkeypatch, request) -> Iterator[Fstab]:
    """
    Mock loading of OpenBSD fstab data from text files
    """
    mock_openbsd_duidmap(monkeypatch)
    yield mock_environment_fstab(monkeypatch, 'openbsd', request.param)


@pytest.fixture(params=MOCK_VARIANTS_OPENBSD)
def openbsd_mountpoints(monkeypatch, request) -> Iterator[Mountpoints]:
    """
    Mock loading of OpenBSD mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'openbsd', request.param)


@pytest.fixture
def fstab_encoded_paths(monkeypatch) -> Iterator[Fstab]:
    """
    Return a demo fstab test file with spaces and tabs encoded in mountpoints
    """
    mock_platform_toolchain(monkeypatch, 'linux')
    monkeypatch.setattr(
        'fs_toolkit.fstab.loader.Fstab.__get_fstab_lines__',
        LoadMockData('linux', 'linux/fstab_encoded')
    )
    yield Fstab()


@pytest.fixture
def unexpected_platform(monkeypatch) -> None:
    """
    Mock unexpected platform information for mountpoints object
    """
    monkeypatch.setattr(
        'fs_toolkit.base.detect_platform_family',
        MockCalledMethod(return_value=UNEXPECTED_PLATFORM)
    )
    monkeypatch.setattr(
        'fs_toolkit.base.detect_toolchain_family',
        MockCalledMethod(return_value=UNEXPECTED_TOOLCHAIN)
    )


@pytest.fixture
def unexpected_toolchain(monkeypatch) -> None:
    """
    Mock unexpected toolchain information for known platform
    """
    monkeypatch.setattr(
        'fs_toolkit.base.detect_platform_family',
        MockCalledMethod(return_value='bsd')
    )
    monkeypatch.setattr(
        'fs_toolkit.base.detect_toolchain_family',
        MockCalledMethod(return_value=UNEXPECTED_TOOLCHAIN)
    )
