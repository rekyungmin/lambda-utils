__all__ = (
    "S3Config",
    "RetriesConfig",
    "ProxiesConfig",
    "Config",
)

from typing import TypedDict, Literal, Union


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
