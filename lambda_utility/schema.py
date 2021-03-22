from __future__ import annotations

__all__ = (
    "camelize",
    "pascalize",
    "BaseSchema",
    "AWSResponseMetadata",
    "S3GetObjectResponse",
    "S3PutObjectResponse",
    "S3HeadObjectResponse",
)

from typing import Dict, Optional

import pydantic


def camelize(s: str) -> str:
    """
    :example:
        >>> camelize("hello_world")
        'helloWorld'
        >>> camelize("e_tag")
        'eTag'
        >>> camelize("_tag")
        'Tag'
    """
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def pascalize(s: str) -> str:
    """
    :example:
        >>> pascalize("hello_world")
        'HelloWorld'
    """
    words = s.split("_")
    return "".join(word.capitalize() for word in words)


class BaseSchema(pydantic.BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class _AWSBaseSchema(pydantic.BaseModel):
    class Config:
        alias_generator = pascalize
        allow_population_by_field_name = True


class AWSResponseMetadata(_AWSBaseSchema):
    request_id: str
    host_id: str
    http_status_code: int = pydantic.Field(..., alias="HTTPStatusCode")
    http_headers: Dict[str, str] = pydantic.Field(..., alias="HTTPHeaders")
    retry_attempts: int


class S3GetObjectResponse(_AWSBaseSchema):
    """
    https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """

    response_metadata: AWSResponseMetadata
    metadata: Dict[str, str]
    content_length: int
    content_type: str
    body: Optional[bytes] = None


class S3PutObjectResponse(_AWSBaseSchema):
    """
    https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
    """

    response_metadata: AWSResponseMetadata
    e_tag: str


class S3HeadObjectResponse(_AWSBaseSchema):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    """

    response_metadata: AWSResponseMetadata
    metadata: Dict[str, str]
    content_length: int
    content_type: str


if __name__ == "__main__":
    import doctest

    doctest.testmod()
