__all__ = (
    "StrPath",
    "CognitoIdentity",
    "ClientContext",
    "LambdaContext",
    "S3Config",
    "RetriesConfig",
    "ProxiesConfig",
    "Config",
)

import os
from typing import Union, Protocol, Optional, TypedDict, Literal

StrPath = Union[str, os.PathLike[str]]


# AWS Lambda Context 정의 시작
# https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
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
    identity: CognitoIdentity  # mobile apps
    client_context: Optional[ClientContext]  # mobile apps

    def get_remaining_time_in_millis(self) -> int:
        ...


# AWS Lambda Context 정의 종료


# botocore.config 정의 시작
# https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
class S3Config(TypedDict, total=False):
    use_accelerate_endpoint: bool
    payload_signing_enabled: bool
    addressing_style: Literal["auto", "virtual", "path"]
    us_east_1_regional_endpoint: Literal["regional", "legacy"]


class RetriesConfig(TypedDict, total=False):
    total_max_attempts: int
    max_attempts: int
    mode: Literal["legacy", "standard", "adaptive"]


class ProxiesConfig(TypedDict, total=False):
    proxy_ca_bundle: str
    proxy_client_cert: Union[str, tuple[str, str]]
    proxy_use_forwarding_for_https: bool


class Config(TypedDict, total=False):
    region_name: str
    signature_version: str
    user_agent: str
    user_agent_extra: str
    connect_timeout: float
    read_timeout: float
    parameter_validation: bool
    max_pool_connections: int
    proxies: dict[str, str]
    proxies_config: ProxiesConfig
    s3: S3Config
    retries: RetriesConfig
    client_cert: Union[str, tuple[str, str]]
    inject_host_prefix: bool


# botocore.config 정의 종료
