from __future__ import annotations

__all__ = (
    "PathExt",
    "classify_directory",
)

import collections
import pathlib

from lambda_utility.typedefs import PathLike


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


def classify_directory(*paths: PathLike) -> dict[str, list[PathExt]]:
    """디렉토리별 path 분류

    디렉토리 depth에 낮은 순서대로 반환한다.
    :example:
        >>> classify_directory("poetry.lock", "pyproject.toml", "lambda_utility/path.py", "lambda_utility/function.py")
        {
            '.': [PathExt('poetry.lock'), PathExt('pyproject.toml')],
            'lambda_utility': [PathExt('lambda_utility/path.py'), PathExt('lambda_utility/function.py')],
        }
    """
    result = collections.defaultdict(list)
    for path in paths:
        if not isinstance(path, PathExt):
            path = PathExt(path)
        result[str(path.parent)].append(path)

    return dict(sorted(result.items(), key=lambda x: x[0].count("/")))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
