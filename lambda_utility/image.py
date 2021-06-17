from __future__ import annotations

__all__ = (
    "calculate_aspect_size",
    "calculate_split_size",
    "resize_width_to_maintain_aspect_ratio",
    "resize_height_to_maintain_aspect_ratio",
    "split_width",
    "split_height",
)

from typing import Optional, Iterator, Protocol, TypeVar, cast

from lambda_utility.utils import round_number

ResizableImageT = TypeVar("ResizableImageT", bound="ResizableImage")


class ResizableImage(Protocol):
    # like `PIL.Image.Image`
    format: Optional[str]

    @property
    def size(self) -> tuple[int, int]:
        ...

    def resize(
        self: ResizableImageT,
        size: tuple[int, int],
        resample: int,
    ) -> ResizableImageT:
        ...

    def crop(self: ResizableImageT, box: tuple[int, int, int, int]) -> ResizableImageT:
        # box: (left, upper, right, lower)
        ...


def calculate_aspect_size(
    src_size: tuple[int, int],
    *,
    target_width: Optional[int] = None,
    target_height: Optional[int] = None,
) -> tuple[int, int]:
    if target_width is None and target_height is None:
        raise ValueError("Either width or height is required")
    if target_width is not None and target_height is not None:
        return target_width, target_height

    src_width, src_height = src_size
    if target_width is not None:
        target_width = cast(int, target_width)
        ratio = target_width / src_width
        return int(target_width), int(round_number(src_height * ratio))
    else:
        target_height = cast(int, target_height)
        ratio = target_height / src_height
        return int(round_number(src_width * ratio)), int(target_height)


def calculate_split_size(total_size: int, max_size: int) -> Iterator[int]:
    total_n, rest = divmod(total_size, max_size)
    if rest != 0:
        total_n += 1

    size, crumb = divmod(total_size, total_n)
    for _ in range(total_n - 1):
        yield size

    yield size + crumb


def _resize_image_to_maintain_aspect_ratio(
    image: ResizableImageT,
    *,
    width: Optional[int] = None,
    height: Optional[int] = None,
    resample: int,
) -> ResizableImageT:
    target_size = calculate_aspect_size(
        image.size, target_width=width, target_height=height
    )
    if image.size != target_size:
        image = image.resize(target_size, resample)
    return image


def resize_width_to_maintain_aspect_ratio(
    image: ResizableImageT, width: int, resample: int
) -> ResizableImageT:
    return _resize_image_to_maintain_aspect_ratio(image, width=width, resample=resample)


def resize_height_to_maintain_aspect_ratio(
    image: ResizableImageT, height: int, resample: int
) -> ResizableImageT:
    return _resize_image_to_maintain_aspect_ratio(
        image, height=height, resample=resample
    )


def split_width(image: ResizableImageT, max_width: int) -> Iterator[ResizableImageT]:
    image_format = image.format
    width, height = image.size
    left = 0
    for width_part in calculate_split_size(width, max_width):
        right = left + width_part
        cropped = image.crop((left, 0, right, height))
        cropped.format = image_format
        yield cropped
        left += width_part


def split_height(image: ResizableImageT, max_height: int) -> Iterator[ResizableImageT]:
    image_format = image.format
    width, height = image.size
    upper = 0
    for height_part in calculate_split_size(height, max_height):
        lower = upper + height_part
        cropped = image.crop((0, upper, width, lower))
        cropped.format = image_format
        yield cropped
        upper += height_part
