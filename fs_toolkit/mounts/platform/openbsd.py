#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
OpenBSD mounpoints
"""
from .bsd import BSDMountpoint, BSDFilesystem, BSDMountPointOptions, BSDMountpointUsage

OPENBSD_VIRTUAL_FILESYSTEMS = (
    'sysfs',
    'procfs',
)


# pylint: disable=too-few-public-methods
class OpenBSDMountpointUsage(BSDMountpointUsage):
    """
    OpenBSD specific mountpoint usage data
    """


# pylint: disable=too-few-public-methods
class OpenBSDMountPointOptions(BSDMountPointOptions):
    """
    OpenBSD specific mountpoint options
    """


# pylint: disable=too-few-public-methods
class OpenBSDFilesystem(BSDFilesystem):
    """
    OpenBSD specific mountpoint options
    """
    virtual_filesystems = OPENBSD_VIRTUAL_FILESYSTEMS


class OpenBSDMountPoint(BSDMountpoint):
    """
    OpenBSD specific mountpoint
    """
    filesystem_class = OpenBSDFilesystem
    options_class = OpenBSDMountPointOptions
    usage_class = OpenBSDMountpointUsage
