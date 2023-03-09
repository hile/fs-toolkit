#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Fstab parser for BSD
"""
from .base import FstabComment, FstabEntry


# pylint: disable=too-few-public-methods
class BSDFstabComment(FstabComment):
    """
    BSD specific class for fstab entries
    """


class BSDFstabEntry(FstabEntry):
    """
    BSD specific class for fstab entries
    """
