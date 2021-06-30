from __future__ import annotations

__all__ = ("invoke",)

from typing import Optional, Literal, Union, BinaryIO, Any

import aiobotocore
import botocore.client

from lambda_utility.session import create_client
from lambda_utility.schema import LambdaInvocationResponse

InvocationType = Literal["Event", "RequestResponse", "DryRun"]
LogType = Literal["None", "Tail"]


class LambdaInvokeError(Exception):
    pass


def is_success_response(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return True

    # TODO: 헤더 또는 다른 검증된 값을 이용하도록 변경 필요
    return "errorMessage" not in payload


async def invoke(
    function_name: str,
    invocation_type: InvocationType,
    payload: Union[bytes, BinaryIO],
    log_type: LogType = "None",
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    raise_exception: bool = True,
) -> LambdaInvocationResponse:
    if client is None:
        client = create_client("lambda", config=config)

    async with client as client_obj:
        resp = await client_obj.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=payload,
        )
        try:
            received_payload_stream = resp.pop("Payload")
            received_payload = await received_payload_stream.read()
        except KeyError:
            received_payload = None

        result = LambdaInvocationResponse(**resp, payload=received_payload)
        if raise_exception and not is_success_response(result.payload):
            raise LambdaInvokeError(str(result.payload))  # TODO: 메시지는 변경될 수 있음

        return result
