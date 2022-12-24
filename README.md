![Unit Tests](https://github.com/hile/fs-toolkit/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/fs-toolkit/actions/workflows/lint.yml/badge.svg)

# Filesystem information tools

This module contains utilities to query local filesystem information as python objects,
including mount points, disk usage and fstab contents.

This tool does similar things as `psutil` package: it may be better suited to
your use and has many features missing from this module.

## Installing

```bash
pip install fs-toolkit
```

## Basic examples

Some usage examples

Fstab:

```bash
from fs_toolkit.fstab import Fstab
fstab = Fstab()
fstab.get_by_mountpoint('/var/my-secrets').uuid
```

Mounts and df (linked together):

```bash
from fs_toolkit.mounts import Mountpoints
print('\n'.join(f'{mp.usage.used:10} {mp.mountpoint}' for mp in Mountpoints()))
```
