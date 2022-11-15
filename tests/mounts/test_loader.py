"""
Unit tests for fs_toolkit.mounts.loader class
"""
import pytest

from sys_toolkit.tests.mock import MockRun

from fs_toolkit.exceptions import FilesystemError
from fs_toolkit.mounts import Mountpoints

from ..conftest import MOCK_DATA

MOCK_MOUNT_FILE = MOCK_DATA.joinpath('freebsd/mount')
MOCK_DF_FILE = MOCK_DATA.joinpath('freebsd/df')


# pylint:disable=too-few-public-methods
class MockRunCommands(MockRun):
    """
    Mock calls to collect data
    """
    def __init__(self, stderr: str = '') -> None:
        super().__init__(encoding='utf-8')
        self.stderr = stderr
        self.mount_data = MOCK_MOUNT_FILE.read_bytes()
        self.df_data = MOCK_DF_FILE.read_bytes()

    def __call__(self, *args, **kwargs):
        """
        Call mocked check_output, storing call argument and returning data from self.path file
        """
        super().__call__(*args, **kwargs)
        if args[0] == 'mount':
            return self.mount_data, self.stderr
        if args[0] == 'df':
            return self.df_data, self.stderr
        raise ValueError(f'Unexpected command arguments: {args}')


# pylint: disable=unused-argument
def test_mountpoints_loader_unexpected_platform(unexpected_platform):
    """
    Test attempts to get Mountpoints object with unexpected platform data
    """
    with pytest.raises(FilesystemError):
        Mountpoints()


# pylint: disable=unused-argument
def test_mountpoints_loader_unexpected_toolchain(unexpected_toolchain):
    """
    Test attempts to get Mountpoints object with known platform and unexpected toolchain data
    """
    with pytest.raises(FilesystemError):
        Mountpoints()


# pylint: disable=unused-argument
def test_mountpoints_loader_get_mount_lines(mock_platform_data, monkeypatch):
    """
    Test calling of __get_mount_lines__ method
    """
    mock_method = MockRunCommands()
    monkeypatch.setattr('fs_toolkit.mounts.loader.run_command', mock_method)

    mountpoints = Mountpoints()
    assert mock_method.call_count == 0

    list(mountpoints)
    assert mock_method.call_count == 2

    # Does not reload the files
    list(mountpoints)
    assert mock_method.call_count == 2
