__all__ = (
    "CognitoIdentity",
    "ClientContext",
    "LambdaContext",
)

from typing import Protocol, Optional


class CognitoIdentity(Protocol):
    """요청을 인가한 Amazon Congnito identity 정보

    ref: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    """

    cognito_identity_id: Optional[str]
    cognito_identity_pool_id: Optional[str]


class ClientContext(Protocol):
    """Client application에서 Lambda에 제공하는 client context

    ref: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    """

    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str
    custom: dict
    env: dict


class LambdaContext(Protocol):
    """Lambda 함수가 실행될 때 핸들러에 전달되는 context object의 인터페이스

    ref: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    """

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
        """실행 시간이 끝나기까지 남은 시간(milliseconds)을 리턴"""
