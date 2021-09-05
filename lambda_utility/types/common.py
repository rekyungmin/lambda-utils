__all__ = ("StrPath",)

import os
from typing import Union

StrPath = Union[str, os.PathLike[str]]
