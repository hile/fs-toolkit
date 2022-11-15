"""
Unit tests configuration for fs_toolkit module
"""
from pathlib import Path

import pytest

from sys_toolkit.tests.mock import MockCalledMethod

from fs_toolkit.fstab import Fstab
from fs_toolkit.mounts import Mountpoints

MOCK_DATA = Path(__file__).parent.joinpath('data')

PLATFORM_MAP = {
    'freebsd': 'bsd',
}
TOOLCHAIN_MAP = {
    'freebsd': 'bsd',
    'darwin': 'bsd',
    'linux': 'gnu',
    'openbsd': 'openbsd',
}

UNEXPECTED_PLATFORM = 'windows'
UNEXPECTED_TOOLCHAIN = 'other'


# pylint: disable=too-few-public-methods
class LoadMockData(MockCalledMethod):
    """
    Load mock data as text lines
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __call__(self, *args, **kwargs):
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
        LoadMockData('openbsd/sysctl.hw.disknames')
    )


def mock_platform_toolchain(monkeypatch, environment: str) -> Mountpoints:
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


def mock_data_loaders(monkeypatch, environment: str) -> Mountpoints:
    """
    Mock mount and df command data outputs
    """
    monkeypatch.setattr(
        'fs_toolkit.fstab.loader.Fstab.__get_fstab_lines__',
        LoadMockData(f'{environment}/fstab')
    )
    monkeypatch.setattr(
        'fs_toolkit.mounts.loader.Mountpoints.__get_mount_lines__',
        LoadMockData(f'{environment}/mount')
    )
    monkeypatch.setattr(
        'fs_toolkit.mounts.loader.Mountpoints.__get_df_lines__',
        LoadMockData(f'{environment}/df')
    )


def mock_environment_fstab(monkeypatch, environment: str) -> Mountpoints:
    """
    Mock specified platform, toolchain and data for Fstab class
    """
    mock_platform_toolchain(monkeypatch, environment)
    mock_data_loaders(monkeypatch, environment)
    return Fstab()


def mock_environment_mountpoints(monkeypatch, environment: str) -> Mountpoints:
    """
    Mock specified platform, toolchain and data for Mountpoints class
    """
    mock_platform_toolchain(monkeypatch, environment)
    mock_data_loaders(monkeypatch, environment)
    return Mountpoints()


@pytest.fixture
def mock_platform_data(monkeypatch) -> Mountpoints:
    """
    Mock platform and toolchain without data
    """
    mock_platform_toolchain(monkeypatch, 'freebsd')
    yield Mountpoints()


@pytest.fixture
def bsd_fstab(monkeypatch) -> Fstab:
    """
    Mock loading of BSD fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'freebsd')


@pytest.fixture
def bsd_mountpoints(monkeypatch) -> Mountpoints:
    """
    Mock loading of BSD mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'freebsd')


@pytest.fixture
def darwin_fstab(monkeypatch) -> Fstab:
    """
    Mock loading of macOS darwin fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'darwin')


@pytest.fixture
def darwin_mountpoints(monkeypatch) -> Mountpoints:
    """
    Mock loading of macOS darwin mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'darwin')


@pytest.fixture
def linux_fstab(monkeypatch) -> Fstab:
    """
    Mock loading of Linux fstab data from text files
    """
    yield mock_environment_fstab(monkeypatch, 'linux')


@pytest.fixture
def linux_mountpoints(monkeypatch) -> Mountpoints:
    """
    Mock loading of Linux mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'linux')


@pytest.fixture
def openbsd_fstab(monkeypatch) -> Fstab:
    """
    Mock loading of OpenBSD fstab data from text files
    """
    mock_openbsd_duidmap(monkeypatch)
    yield mock_environment_fstab(monkeypatch, 'openbsd')


@pytest.fixture
def openbsd_mountpoints(monkeypatch) -> Mountpoints:
    """
    Mock loading of OpenBSD mountpoints data from text files
    """
    yield mock_environment_mountpoints(monkeypatch, 'openbsd')


@pytest.fixture
def fstab_encoded_paths(monkeypatch) -> Fstab:
    """
    Return a demo fstab test file with spaces and tabs encoded in mountpoints
    """
    mock_platform_toolchain(monkeypatch, 'linux')
    monkeypatch.setattr(
        'fs_toolkit.fstab.loader.Fstab.__get_fstab_lines__',
        LoadMockData('linux/fstab_encoded')
    )
    yield Fstab()


@pytest.fixture
def unexpected_platform(monkeypatch):
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
def unexpected_toolchain(monkeypatch):
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
