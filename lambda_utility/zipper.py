from __future__ import annotations

__all__ = ("Unzip",)

import functools
import re
import zipfile
from collections.abc import Iterable, Callable
from types import TracebackType
from typing import Optional, Type, Union

from lambda_utility.typedefs import PathLike


class Unzip:
    zip_path: str
    zip_ref: zipfile.ZipFile
    includes: Iterable[Union[re.Pattern, Callable[[str], bool]]]
    excludes: Iterable[Union[re.Pattern, Callable[[str], bool]]]

    def __init__(
        self,
        zip_path: PathLike,
        *,
        includes: Optional[Iterable[Union[re.Pattern, Callable[[str], bool]]]] = None,
        excludes: Optional[Iterable[Union[re.Pattern, Callable[[str], bool]]]] = None,
    ):
        self.zip_path = str(zip_path)
        self.includes = includes if includes is not None else []
        self.excludes = excludes if excludes is not None else []

    def __enter__(self):
        self.zip_ref = zipfile.ZipFile(self.zip_path).__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.zip_ref.__exit__(exc_type, exc_value, traceback)

    def __call__(
        self,
        *,
        path: Optional[PathLike] = None,
        files: Optional[Iterable[str]] = None,
        pwd: Optional[bytes] = None,
    ) -> list[str]:
        if path is not None:
            path = str(path)

        if files is None:
            files = self.get_valid_namelist()

        self.zip_ref.extractall(path=path, members=files, pwd=pwd)
        return list(files)

    @functools.lru_cache
    def get_valid_namelist(self) -> list[str]:
        return [
            zipped_file
            for zipped_file in self.get_namelist()
            if self.check_includes(zipped_file) and not self.check_excludes(zipped_file)
        ]

    @functools.lru_cache
    def get_namelist(self) -> list[str]:
        return self.zip_ref.namelist()

    def check_excludes(self, filename: PathLike) -> bool:
        filename = str(filename)
        for exclude in self.excludes:
            if isinstance(exclude, re.Pattern):
                if exclude.search(filename):
                    return True
            elif callable(exclude):
                if exclude(filename):
                    return True
        return False

    def check_includes(self, filename: PathLike) -> bool:
        filename = str(filename)
        for include in self.includes:
            if isinstance(include, re.Pattern):
                if not include.search(filename):
                    return False
            elif callable(include):
                if not include(filename):
                    return False
        return True
