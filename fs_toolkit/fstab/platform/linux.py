#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Fstab parser for linux
"""
from .base import FstabComment, FstabEntry


# pylint: disable=too-few-public-methods
class LinuxFstabComment(FstabComment):
    """
    Linux specific class for fstab entries
    """


class LinuxFstabEntry(FstabEntry):
    """
    Linux specific class for fstab entries
    """
