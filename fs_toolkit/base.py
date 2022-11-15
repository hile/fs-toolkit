"""
Common base class for line parser output data classes
"""
import re

from typing import List

from sys_toolkit.collection import CachedMutableSequence
from sys_toolkit.platform import detect_platform_family, detect_toolchain_family


class LineLoader(CachedMutableSequence):
    """
    Loader for line based data to cached mutable sequence
    """
    def __init__(self) -> None:
        super().__init__()
        self.__platform__ = detect_platform_family()
        self.__toolchain__ = detect_toolchain_family()
        self.__iter_items__ = None

    def __iter__(self):
        if not self.__loaded__:
            self.update()
        return iter(self.__items__)

    def __next__(self):
        if self.__iter_items__ is None:
            if not self.__loaded__:
                self.update()
            self.__iter_items__ = iter(self.__items__)
        try:
            return next(self.__iter_items__)
        except StopIteration as error:
            self.__iter_items__ = None
            raise StopIteration from error

    def __match_pattern_list__(self, lines: List[str], patterns: List[re.Pattern]) -> List[dict]:
        """
        Match lines to list of grouped regexp patterns, returning list
        of regexp groupdict matches.

        Lines must be iterable of strings and iterable of re.Pattern
        """
        assert isinstance(patterns, list)
        for pattern in patterns:
            assert isinstance(pattern, re.Pattern)
        matches = []
        for line in lines:
            assert isinstance(line, str)
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    matches.append(match.groupdict())
                    break
        return matches

    def update(self):
        """
        Require update to be implemented in child class
        """
        raise NotImplementedError
