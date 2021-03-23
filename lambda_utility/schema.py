from __future__ import annotations

__all__ = (
    "camelize",
    "pascalize",
    "Base64String",
    "JsonString",
    "BaseSchema",
    "AWSResponseMetadata",
    "S3GetObjectResponse",
    "S3PutObjectResponse",
    "S3HeadObjectResponse",
    "LambdaInvocationResponse",
)

import base64
import json
from typing import Dict, Optional, AnyStr, Any, cast

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


class Base64String(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: AnyStr) -> str:
        if not isinstance(v, (str, bytes)):
            raise TypeError("string required")

        try:
            v_bytes = v if isinstance(v, bytes) else cast(str, v).encode()
            binary_text = base64.b64decode(v_bytes)
            text = binary_text.decode()
        except Exception:
            raise ValueError("invalid base64 string format")

        return text

    def __repr__(self):
        return f"Base64String({super().__repr__()})"


class JsonString:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Optional[AnyStr]) -> Any:
        if not isinstance(v, (str, bytes)):
            raise TypeError("string required")

        try:
            v_str = v if isinstance(v, str) else cast(bytes, v).decode()
            return json.JSONDecoder().decode(v_str)
        except Exception:
            raise ValueError("invalid JSON string format")


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


class LambdaInvocationResponse(_AWSBaseSchema):
    """
    https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html?highlight=invoke#Lambda.Client.invoke
    """

    response_metadata: AWSResponseMetadata
    status_code: int
    payload: Optional[JsonString] = None
    executed_version: Optional[str] = None
    function_error: Optional[str] = None
    log_result: Optional[Base64String] = None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
