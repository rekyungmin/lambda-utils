from __future__ import annotations

__all__ = ("PathExt",)

import pathlib


class PathExt(pathlib.PosixPath):
    __slots__ = ()

    def with_stem(self, stem: str) -> PathExt:
        """
        :example:
            >>> str(PathExt("tmp/hello.jpg").with_stem("world"))
            'tmp/world.jpg'
        """
        return self.with_name(stem + self.suffix)

    def append_stem(self, stem: str, *, tail: bool = True) -> PathExt:
        """
        :example:
            >>> str(PathExt("tmp/hello.jpg").append_stem("world", tail=True))
            'tmp/helloworld.jpg'
            >>> str(PathExt("tmp/hello.jpg").append_stem("world", tail=False))
            'tmp/worldhello.jpg'
        """
        new_stem = self.stem + stem if tail else stem + self.stem
        return self.with_stem(new_stem)

    def replace_parent(self, parent: str) -> PathExt:
        """
        :example:
            >>> str(PathExt("tmp/hello.jpg").replace_parent("opt"))
            'opt/hello.jpg'
        """
        return self.parent.parent / parent / self.name

    def append_parent(self, parent: str) -> PathExt:
        """
        :example:
            >>> str(PathExt("tmp/hello.jpg").append_parent("2x"))
            'tmp/2x/hello.jpg'
        """
        return self.parent / parent / self.name


if __name__ == "__main__":
    import doctest

    doctest.testmod()
