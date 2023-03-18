#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Python utility to load mountpoints, disk usage and fstab entry information
"""
# flake8: noqa: F401
from .fstab.loader import Fstab
from .mounts.loader import Mountpoints
