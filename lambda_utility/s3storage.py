from __future__ import annotations

__all__ = (
    "ACL",
    "download_object",
    "download_file",
    "upload_object",
    "upload_file",
    "fetch_head",
    "fetch_meta",
    "ctx_download_file",
)

import contextlib
import enum
import functools
import io
import tempfile
from collections.abc import Callable
from typing import Union, Optional, Any, Iterator

import boto3.s3.transfer

from lambda_utility import _session, path

PathLike = Union[str, path.PathExt]


class ACL(enum.Enum):
    PRIVATE = "private"
    PUBLIC_READ = "public-read"
    PUBLIC_READ_AND_WRITE = "public-read-and-write"


@functools.lru_cache
def get_client(**config: Any):
    return _session.get_client("s3", **config)


def download_object(
    bucket: str,
    key: PathLike,
    *,
    extra: Optional[dict[str, str]] = None,
    callback: Optional[Callable] = None,
    config: Optional[boto3.s3.transfer.TransferConfig] = None,
    session_config: Optional[dict[str, Any]] = None,
) -> bytes:
    if session_config is None:
        session_config = {}

    stream = io.BytesIO()
    session = get_client(**session_config)
    session.download_fileobj(
        Bucket=bucket,
        Key=str(key),
        Fileobj=stream,
        ExtraArgs=extra,
        Callback=callback,
        Config=config,
    )
    return stream.getvalue()


def download_file(
    bucket: str,
    key: PathLike,
    filename: PathLike,
    *,
    extra: Optional[dict[str, str]] = None,
    callback: Optional[Callable] = None,
    config: Optional[boto3.s3.transfer.TransferConfig] = None,
    session_config: Optional[dict[str, Any]] = None,
) -> bytes:
    if session_config is None:
        session_config = {}

    stream = io.BytesIO()
    session = get_client(**session_config)
    session.download_file(
        Bucket=bucket,
        Key=str(key),
        Filename=str(filename),
        ExtraArgs=extra,
        Callback=callback,
        Config=config,
    )
    return stream.getvalue()


def upload_object(
    bucket: str,
    key: PathLike,
    data: bytes,
    *,
    acl: ACL = ACL.PUBLIC_READ,
    extra: Optional[dict[str, str]] = None,
    callback: Optional[Callable] = None,
    config: Optional[boto3.s3.transfer.TransferConfig] = None,
    session_config: Optional[dict[str, Any]] = None,
) -> None:
    if extra is None:
        extra = {}
    if session_config is None:
        session_config = {}

    session = get_client(**session_config)
    stream = io.BytesIO(data)
    session.upload_fileobj(
        Bucket=bucket,
        Key=str(key),
        Fileobj=stream,
        ExtraArgs={**extra, "ACL": acl.value},
        Callback=callback,
        Config=config,
    )


def upload_file(
    bucket: str,
    key: PathLike,
    filename: PathLike,
    *,
    acl: ACL = ACL.PUBLIC_READ,
    extra: Optional[dict[str, str]] = None,
    callback: Optional[Callable] = None,
    config: Optional[boto3.s3.transfer.TransferConfig] = None,
    session_config: Optional[dict[str, Any]] = None,
) -> None:
    if extra is None:
        extra = {}
    if session_config is None:
        session_config = {}

    session = get_client(**session_config)
    session.upload_file(
        Bucket=bucket,
        Key=str(key),
        Filename=str(filename),
        ExtraArgs={**extra, "ACL": acl.value},
        Callback=callback,
        Config=config,
    )


def fetch_head(
    bucket: str,
    key: PathLike,
    *,
    session_config: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    if session_config is None:
        session_config = {}

    session = get_client(**session_config)
    return session.head_object(Bucket=bucket, Key=str(key), **kwargs)


def fetch_meta(
    bucket: str,
    key: PathLike,
    session_config: Optional[dict[str, Any]] = None,
    **kwargs,
) -> dict[str, Any]:
    head = fetch_head(bucket, key, session_config=session_config, **kwargs)
    return head.get("Metadata", {})


@contextlib.contextmanager
def ctx_download_file(
    bucket: str,
    key: PathLike,
    *,
    extra: Optional[dict[str, str]] = None,
    callback: Optional[Callable] = None,
    config: Optional[boto3.s3.transfer.TransferConfig] = None,
    session_config: Optional[dict[str, Any]] = None,
) -> Iterator[path.PathExt]:
    suffix = path.PathExt(key).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        filename = path.PathExt(f.name)
        download_file(
            bucket,
            key,
            filename,
            extra=extra,
            callback=callback,
            config=config,
            session_config=session_config,
        )
        yield filename
