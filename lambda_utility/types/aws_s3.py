__all__ = (
    "S3GetObjectRequest",
    "S3GetObjectResponse",
    "S3HeadObjectRequest",
    "S3HeadObjectResponse",
    "S3PutObjectRequest",
    "S3PutObjectResponse",
)

import datetime
from typing import TypedDict, Any, Literal, Union, IO

from aiobotocore.response import StreamingBody

ResponseMetadata = dict[str, Any]
ServerSideEncryption = Literal["AES256", "aws:kms"]
ReplicationStatus = Literal["COMPLETE", "PENDING", "FAILED", "REPLICA"]
ObjectLockMode = Literal["GOVERNANCE", "COMPLIANCE"]
StorageClass = Literal[
    "STANDARD",
    "REDUCED_REDUNDANCY",
    "STANDARD_IA",
    "ONEZONE_IA",
    "INTELLIGENT_TIERING",
    "GLACIER",
    "DEEP_ARCHIVE",
    "OUTPOSTS",
]
ACL = Literal[
    "private",  # default
    "public-read",
    "public-read-write",
    "authenticated-read",
    "aws-exec-read",
    "bucket-owner-read",
    "bucket-owner-full-control",
]


class S3GetObjectRequest(TypedDict, total=False):
    """get_object의 request parameters

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """

    Bucket: str
    IfMatch: str
    IfModifiedSince: datetime.datetime
    IfNoneMatch: str
    IfUnmodifiedSince: datetime.datetime
    Key: str
    Range: str
    ResponseCacheControl: str
    ResponseContentDisposition: str
    ResponseContentEncoding: str
    ResponseContentLanguage: str
    ResponseContentType: str
    ResponseExpires: datetime.datetime
    VersionId: str
    SSECustomerAlgorithm: str
    SSECustomerKey: str
    RequestPayer: Literal["requester"]
    PartNumber: int
    ExpectedBucketOwner: str


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
    ServerSideEncryption: ServerSideEncryption
    Metadata: dict[str, str]
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    BucketKeyEnabled: bool
    StorageClass: StorageClass
    RequestCharged: str
    ReplicationStatus: ReplicationStatus
    PartsCount: int
    TagCount: int
    ObjectLockMode: ObjectLockMode
    ObjectLockRetainUntilDate: datetime.datetime
    ObjectLockLegalHoldStatus: str


class S3HeadObjectRequest(TypedDict, total=False):
    """head_object의 request parameters

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    """

    Bucket: str
    IfMatch: str
    IfModifiedSince: datetime.datetime
    IfNoneMatch: str
    IfUnmodifiedSince: datetime.datetime
    Key: str
    Range: str
    VersionId: str
    SSECustomerAlgorithm: str
    SSECustomerKey: str
    RequestPayer: Literal["requester"]
    PartNumber: int
    ExpectedBucketOwner: str


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
    StorageClass: StorageClass
    RequestCharged: str
    ReplicationStatus: ReplicationStatus
    PartsCount: int
    ObjectLockMode: ObjectLockMode
    ObjectLockRetainUntilDate: datetime.datetime
    ObjectLockLegalHoldStatus: str

    ResponseMetadata: ResponseMetadata


class S3PutObjectRequest(TypedDict, total=False):
    """put_object의 request parameters

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """

    ACL: ACL
    Body: Union[bytes, IO]
    Bucket: str
    CacheControl: str
    ContentDisposition: str
    ContentEncoding: str
    ContentLanguage: str
    ContentLength: int
    ContentMD5: str
    ContentType: str
    Expires: datetime.datetime
    GrantFullControl: str
    GrantRead: str
    GrantReadACP: str
    GrantWriteACP: str
    Key: str
    Metadata: dict[str, str]
    ServerSideEncryption: ServerSideEncryption
    StorageClass: StorageClass
    WebsiteRedirectLocation: str
    SSECustomerAlgorithm: str
    SSECustomerKey: str
    SSEKMSKeyId: str
    SSEKMSEncryptionContext: str
    BucketKeyEnabled: bool
    RequestPayer: Literal["requester"]
    Tagging: str
    ObjectLockMode: ObjectLockMode
    ObjectLockRetainUntilDate: datetime.datetime
    ObjectLockLegalHoldStatus: Literal["ON", "OFF"]
    ExpectedBucketOwner: str


class S3PutObjectResponse(TypedDict, total=False):
    """put_object의 response structure

    ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """

    ResponseMetadata: ResponseMetadata
    Expiration: str
    ETag: str
    ServerSideEncryption: ServerSideEncryption
    VersionId: str
    SSECustomerAlgorithm: str
    SSECustomerKeyMD5: str
    SSEKMSKeyId: str
    SSEKMSEncryptionContext: str
    BucketKeyEnabled: str
    RequestCharged: Literal["requester"]
