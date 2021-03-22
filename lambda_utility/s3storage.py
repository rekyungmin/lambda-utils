from __future__ import annotations

__all__ = (
    "DEFAULT_CONFIG",
    "create_client",
    "download_object",
    "download_file",
    "upload_object",
    "upload_file",
    "fetch_head",
    "ctx_download_file",
)

import contextlib
import tempfile
from typing import Any, Optional, Literal, BinaryIO, Union, AsyncIterator

import aiobotocore
import botocore.client

from lambda_utility.path import PathExt
from lambda_utility.schema import (
    S3GetObjectResponse,
    S3PutObjectResponse,
    S3HeadObjectResponse,
)
from lambda_utility.typedefs import PathLike

DEFAULT_CONFIG = botocore.client.Config(connect_timeout=600, read_timeout=600)


def create_client(
    service_name: str,
    region_name: Optional[str] = None,
    api_version: Optional[str] = None,
    use_ssl: bool = True,
    verify: Optional[Union[bool, str]] = None,
    endpoint_url: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    config: Optional[botocore.client.Config] = None,
) -> aiobotocore.session.ClientCreatorContext:
    session = aiobotocore.get_session()
    if config:
        config = DEFAULT_CONFIG.merge(config)

    return session.create_client(
        service_name,
        region_name=region_name,
        api_version=api_version,
        use_ssl=use_ssl,
        verify=verify,
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        config=config,
    )


async def download_object(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3GetObjectResponse:
    """
    :exception: botocore.errorfactory.NoSuchBucket
    :exception: botocore.errorfactory.NoSuchKey
    """
    if client is None:
        client = create_client("s3", config=config)

    async with client as client_obj:
        resp = await client_obj.get_object(Bucket=bucket, Key=str(key), **kwargs)

        body = await resp["Body"].read()
        return S3GetObjectResponse(
            content_type=resp["ContentType"],
            content_length=resp["ContentLength"],
            response_metadata=resp["ResponseMetadata"],
            metadata=resp["Metadata"],
            body=body,
        )


async def download_file(
    bucket: str,
    key: PathLike,
    filename: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> S3GetObjectResponse:
    data = await download_object(bucket, key, client=client, config=config)
    with open(filename, "wb") as f:
        f.write(data.body or b"")

    data.body = None
    return data


ACLType = Literal[
    "private",
    "public-read",
    "public-read-write",
    "authenticated-read",
    "aws-exec-read",
    "bucket-owner-read",
    "bucket-owner-full-control",
]


async def upload_object(
    bucket: str,
    key: PathLike,
    body: Union[bytes, BinaryIO],
    *,
    acl: ACLType = "private",
    metadata: Optional[dict[str, str]] = None,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3PutObjectResponse:
    if client is None:
        client = create_client("s3", config=config)

    if metadata is None:
        metadata = {}

    async with client as client_obj:
        resp = await client_obj.put_object(
            Bucket=bucket, Key=str(key), Body=body, ACL=acl, Metadata=metadata, **kwargs
        )
        return S3PutObjectResponse(**resp)


async def upload_file(
    bucket: str,
    key: PathLike,
    filepath: PathLike,
    *,
    acl: ACLType = "private",
    metadata: Optional[dict[str, str]] = None,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3PutObjectResponse:
    with open(filepath, "rb") as f:
        return await upload_object(
            bucket,
            key,
            f,
            acl=acl,
            metadata=metadata,
            client=client,
            config=config,
            **kwargs,
        )


async def fetch_head(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    **kwargs: Any,
) -> S3HeadObjectResponse:
    if client is None:
        client = create_client("s3", config=config)

    async with client as client_obj:
        resp = await client_obj.head_object(Bucket=bucket, Key=str(key), **kwargs)
        return S3HeadObjectResponse(**resp)


@contextlib.asynccontextmanager
async def ctx_download_file(
    bucket: str,
    key: PathLike,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> AsyncIterator[tuple[PathExt, S3GetObjectResponse]]:
    suffix = PathExt(key).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        resp = await download_object(bucket, key, client=client, config=config)
        f.write(resp.body or b"")
        resp.body = None
        yield PathExt(f.name), resp
