#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Fstab parser for macOS Darwin
"""
from .base import FstabComment, FstabEntry


# pylint: disable=too-few-public-methods
class DarwinFstabComment(FstabComment):
    """
    Darwin specific class for fstab entries
    """


class DarwinFstabEntry(FstabEntry):
    """
    Darwin specific class for fstab entries
    """
