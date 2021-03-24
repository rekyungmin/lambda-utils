from __future__ import annotations

__all__ = (
    "PathLike",
    "CognitoIdentity",
    "ClientContext",
    "LambdaContext",
)

import pathlib
from typing import Union, Protocol, Optional

PathLike = Union[str, pathlib.PurePath]


class CognitoIdentity(Protocol):
    cognito_identity_id: Optional[str]
    cognito_identity_pool_id: Optional[str]


class ClientContext(Protocol):
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str
    custom: dict
    env: dict


class LambdaContext(Protocol):
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: str
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: CognitoIdentity
    client_context: Optional[ClientContext]

    def get_remaining_time_in_millis(self) -> int:
        ...
