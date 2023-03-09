#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Linux mountpoints
"""
from .base import Mountpoint, Filesystem, MountpointOptions, MountpointUsage

LINUX_VIRTUAL_FILESYSTEMS = (
    'autofs',
    'binfmt_misc',
    'bpf',
    'cgroup',
    'cgroup2',
    'configfs',
    'debugfs',
    'devpts',
    'devtmpfs',
    'efivarfs',
    'fusectl',
    'hugetlbfs',
    'mqueue',
    'nsfs',
    'overlay',
    'proc',
    'procfs',
    'pstore',
    'ramfs',
    'rpc_pipefs',
    'securityfs',
    'selinuxfs',
    'sysfs',
    'tmpfs',
    'tracefs',
)


# pylint: disable=too-few-public-methods
class LinuxMountpointUsage(MountpointUsage):
    """
    Linux specific mountpoint usage data
    """


# pylint: disable=too-few-public-methods
class LinuxMountPointOptions(MountpointOptions):
    """
    Linux specific mountpoint options
    """


# pylint: disable=too-few-public-methods
class LinuxFilesystem(Filesystem):
    """
    Linux specific mountpoint options
    """
    virtual_filesystems = LINUX_VIRTUAL_FILESYSTEMS


class LinuxMountPoint(Mountpoint):
    """
    Linux specific mountpoint
    """
    filesystem_class = LinuxFilesystem
    options_class = LinuxMountPointOptions
    usage_class = LinuxMountpointUsage
