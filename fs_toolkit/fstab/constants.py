#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Constants for fstab loading
"""
from pathlib import Path

FSTAB_PATH = Path('/etc/fstab')

FSTAB_FILE_NONE_VALUES = (
    'none',
)

FSTAB_FIELDS = (
    'fs_spec',
    'fs_file',
    'fs_vfstype',
    'fs_mntops',
    'fs_freq',
    'fs_passno',
)
FSTAB_INT_FIELDS = (
    'fs_freq',
    'fs_passno',
)
