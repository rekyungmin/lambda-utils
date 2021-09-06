__all__ = ("Session",)

from typing import Optional, Union, Any

from aiobotocore.config import AioConfig
from aiobotocore.credentials import AioCredentials
from aiobotocore.session import ClientCreatorContext, get_session, AioSession

from lambda_utility.types.aws_config import Config


class Session:
    """Config를 저장하고 service client를 생성할 수 있게 한다."""

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[None] = None,
        profile_name: Optional[str] = None,
    ):
        """
        :param aws_access_key_id: AWS access key id
        :param aws_secret_access_key: AWS secret key id
        :param aws_session_token: AWS temporary session token
        :param region_name: 새 커넥션을 만들 때 default region
        :param profile_name: 사용할 profile name.
            `None`일 경우 default profile이 사용된다.
            공유 자격 증명 파일의 기본 위치: `~/.aws/credentials`
        """
        self._aio_session: AioSession = get_session()
        if aws_access_key_id or aws_secret_access_key or aws_session_token:
            self._aio_session.set_credentials(
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                token=aws_session_token,
            )

        if region_name is not None:
            self._aio_session.set_config_variable("region", region_name)

        if profile_name is not None:
            self._aio_session.set_config_variable("profile", profile_name)

    @property
    def aio_session(self) -> AioSession:
        """AioSession 객체에 직접 접근 (readonly)"""
        return self._aio_session

    @property
    def profile_name(self) -> str:
        """프로필 이름(readonly)"""
        return self.aio_session.profile or "default"

    @property
    def region_name(self) -> str:
        """리전 이름(readonly)"""
        return self.aio_session.get_config_variable("region")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(region_name={self.region_name}, profile_name={self.profile_name})"

    async def get_credentials(self) -> Optional[AioCredentials]:
        """AWS 자격 증명 정보를 가져온다.

        자격 증명을 아직 로딩되지 않았다면 로딩을 수행한다.
        이미 로딩된 경우 캐시된 자격 증명이 반환된다.
        """
        return await self.aio_session.get_credentials()

    def create_client(
        self,
        service_name: str,
        region_name: Optional[str] = None,
        api_version: Optional[str] = None,
        use_ssl: bool = True,
        verify: Optional[Union[bool, str]] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        config: Optional[Union[AioConfig, Config]] = None,
        **kwargs: Any,
    ) -> ClientCreatorContext:
        """aiobotocore 클라이언트 객체를 생성한다.

        :param service_name: 서비스 이름 (예를 들어 "s3", "ec2")
        :param region_name: 클라이언트와 연결된 리전 이름.
            클라이언트는 단일 리전과 연결된다.
        :param api_version: 사용할 API 버전.
            기본적으로 botocore는 클라이언트를 생성할 때 최신 API 버전을 사용한다.
            이전 버전의 API를 사용하려는 경우에만 이 파라미터를 사용한다.
        :param use_ssl: SSL 사용 여부.
            기본적으로 SSL이 사용된다.
            모든 서비스가 non-ssl 커넥션을 지원하는 것은 아니다.
        :param verify: SSL certificates 검증 여부.
            기본적으로 SSL 인증서가 검증된다.
            다음과 같은 값을 전달할 수 있다:
                * False - SSL certificates의 유효성을 검사하지 않는다.
                  SSL은 여전히 사용되지만(`use_ssl`이 False인 경우 제외) SSL 인증서는 검증되지 않는다.
                * path/to/cert/bundle.pem - 사용할 CA cert 번들의 파일 이름.
                  botocore에서 사용하는 것과 다른 CA cert 번들을 사용하려는 경우 이 인자를 사용한다.
        :param endpoint_url: 구성된 클라이언트에 사용할 전체 URL.
            일반적으로 botocore는 서비스와 통신할 때 적절한 URL을 자동으로 구성한다.
            전체 URL("http/https" scheme 포함)을 지정하여 이 동작을 재정의할 수 있다.
            이 값이 제공되면 `use_ssl`이 무시된다.
        :param aws_access_key_id: 클라이언트를 생성할 때 사용할 액세스 키.
            이 인자가 제공되지 않으면 세션에 구성된 자격 증명이 자동으로 사용된다.
            특정 클라이언트의 자격 증명을 재정의하려는 경우에만 이 인자를 제공한다.
        :param aws_secret_access_key: 클라이언트를 생성할 때 사용할 시크릿 키.
            이 인자가 제공되지 않으면 세션에 구성된 자격 증명이 자동으로 사용된다.
            특정 클라이언트의 자격 증명을 재정의하려는 경우에만 이 인자를 제공한다.
        :param aws_session_token: 클라이언트를 생성할 때 사용할 세션 토큰.
            이 인자가 제공되지 않으면 세션에 구성된 자격 증명이 자동으로 사용된다.
            특정 클라이언트의 자격 증명을 재정의하려는 경우에만 이 인자를 제공한다.
        :param config: 고급 클라이언트 configuration 옵션.
            `region_name`이 클라이언트 config에 지정된 경우,
             해당 값은 환경 변수 및 configuration 값보다 우선하지만
             메서드에 명시적으로 전달된 `region_name` 값보다 우선하지는 않는다.
        :param kwargs: 추가 옵션.
            aiobotocore에 새로운 파라미터가 생기거나,
            기존 파라미터 이름이 변경된 경우 경우 사용한다.
        """
        return self.aio_session.create_client(
            service_name,
            region_name=region_name,
            api_version=api_version,
            use_ssl=use_ssl,
            verify=verify,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            config=AioConfig(**config) if isinstance(config, dict) else config,
            **kwargs,
        )
