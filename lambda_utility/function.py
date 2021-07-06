from __future__ import annotations

__all__ = ("invoke",)

from typing import Optional, Literal, Union, BinaryIO, Dict

import aiobotocore
import botocore.client

from lambda_utility.schema import LambdaInvocationResponse
from lambda_utility.session import create_client


class LambdaFunctionError(Exception):
    pass


def _is_success_response(header: Dict) -> bool:
    return "x-amz-function-error" not in header


async def invoke(
    function_name: str,
    invocation_type: Literal["Event", "RequestResponse", "DryRun"],
    payload: Union[bytes, BinaryIO],
    log_type: Literal["None", "Tail"] = "None",
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
    raise_function_error: bool = True,
) -> LambdaInvocationResponse:
    """Invokes a Lambda function.
    You can invoke a function synchronously (and wait for the response),
    or asynchronously. To invoke a function asynchronously, set InvocationType to Event.

    :ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html?highlight=invoke#Lambda.Client.invoke
    :exception: Lambda.Client.exceptions.ServiceException
    :exception: Lambda.Client.exceptions.ResourceNotFoundException
    :exception: Lambda.Client.exceptions.InvalidRequestContentException
    :exception: Lambda.Client.exceptions.RequestTooLargeException
    :exception: Lambda.Client.exceptions.UnsupportedMediaTypeException
    :exception: Lambda.Client.exceptions.TooManyRequestsException
    :exception: Lambda.Client.exceptions.InvalidParameterValueException
    :exception: Lambda.Client.exceptions.EC2UnexpectedException
    :exception: Lambda.Client.exceptions.SubnetIPAddressLimitReachedException
    :exception: Lambda.Client.exceptions.ENILimitReachedException
    :exception: Lambda.Client.exceptions.EFSMountConnectivityException
    :exception: Lambda.Client.exceptions.EFSMountFailureException
    :exception: Lambda.Client.exceptions.EFSMountTimeoutException
    :exception: Lambda.Client.exceptions.EFSIOException
    :exception: Lambda.Client.exceptions.EC2ThrottledException
    :exception: Lambda.Client.exceptions.EC2AccessDeniedException
    :exception: Lambda.Client.exceptions.InvalidSubnetIDException
    :exception: Lambda.Client.exceptions.InvalidSecurityGroupIDException
    :exception: Lambda.Client.exceptions.InvalidZipFileException
    :exception: Lambda.Client.exceptions.KMSDisabledException
    :exception: Lambda.Client.exceptions.KMSInvalidStateException
    :exception: Lambda.Client.exceptions.KMSAccessDeniedException
    :exception: Lambda.Client.exceptions.KMSNotFoundException
    :exception: Lambda.Client.exceptions.InvalidRuntimeException
    :exception: Lambda.Client.exceptions.ResourceConflictException
    :exception: Lambda.Client.exceptions.ResourceNotReadyException
    """
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
        if raise_function_error and not _is_success_response(
            resp["ResponseMetadata"]["HTTPHeaders"]
        ):
            raise LambdaFunctionError(str(result.payload))

        return result
