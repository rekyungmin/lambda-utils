__all__ = (
    "S3GetObjectResponse",
    "S3HeadObjectResponse",
    "S3PutObjectResponse",
)

import datetime
from typing import TypedDict, Any, Literal

from aiobotocore.response import StreamingBody


ResponseMetadata = dict[str, Any]


class S3GetObjectResponse(TypedDict, total=False):
    """get_object의 response structure

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """

    ResponseMetadata: ResponseMetadata
    Body: StreamingBody
    DeleteMarker: bool
    AcceptRanges: str
    Expiration: str
    Restore: str
    LastModified: datetime.datetime
    ContentLength: int
    ETag: str
    MissingMeta: int
    VersionId: str
    CacheControl: str
    ContentDisposition: str
    ContentEncoding: str
    ContentLanguage: str
    ContentRange: str
    ContentType: str
    Expires: datetime.datetime
    WebsiteRedirectLocation: str
    ServerSideEncryption: Literal["AES256", "aws:kms"]
    Metadata: dict[str, str]
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    BucketKeyEnabled: bool
    StorageClass: Literal[
        "STANDARD",
        "REDUCED_REDUNDANCY",
        "STANDARD_IA",
        "ONEZONE_IA",
        "INTELLIGENT_TIERING",
        "GLACIER",
        "DEEP_ARCHIVE",
        "OUTPOSTS",
    ]
    RequestCharged: str
    ReplicationStatus: Literal["COMPLETE", "PENDING", "FAILED", "REPLICA"]
    PartsCount: int
    TagCount: int
    ObjectLockMode: Literal["GOVERNANCE", "COMPLIANCE"]
    ObjectLockRetainUntilDate: datetime.datetime
    ObjectLockLegalHoldStatus: str


class S3HeadObjectResponse(TypedDict, total=False):
    """head_object의 response structure

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    """

    DeleteMarker: bool
    AcceptRanges: str
    Expiration: str
    Restore: str
    ArchiveStatus: Literal["ARCHIVE_ACCESS", "DEEP_ARCHIVE_ACCESS"]
    LastModified: datetime.datetime
    ContentLength: int
    ETag: str
    MissingMeta: int
    VersionId: str
    CacheControl: str
    ContentDisposition: str
    ContentEncoding: str
    ContentLanguage: str
    ContentType: str
    Expires: datetime.datetime
    WebsiteRedirectLocation: str
    ServerSideEncryption: str
    Metadata: dict[str, str]
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    BucketKeyEnabled: bool
    StorageClass: Literal[
        "STANDARD",
        "REDUCED_REDUNDANCY",
        "STANDARD_IA",
        "ONEZONE_IA",
        "INTELLIGENT_TIERING",
        "GLACIER",
        "DEEP_ARCHIVE",
        "OUTPOSTS",
    ]
    RequestCharged: str
    ReplicationStatus: Literal["COMPLETE", "PENDING", "FAILED", "REPLICA"]
    PartsCount: int
    ObjectLockMode: Literal["GOVERNANCE", "COMPLIANCE"]
    ObjectLockRetainUntilDate: datetime.datetime
    ObjectLockLegalHoldStatus: str

    ResponseMetadata: ResponseMetadata


class S3PutObjectResponse(TypedDict, total=False):
    """put_object의 response structure

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """

    ResponseMetadata: ResponseMetadata
    Expiration: str
    ETag: str
    ServerSideEncryption: Literal["AES256", "aws:kms"]
    VersionId: str
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    SSEKMSEncryptionContext: str
    BucketKeyEnabled: str
    RequestCharged: Literal["requester"]
