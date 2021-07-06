from __future__ import annotations

__all__ = (
    "get_queue_url",
    "send_message",
    "delete_message",
    "receive_message",
)

from typing import Optional, Any

import aiobotocore
import botocore.client

from lambda_utility.schema import SQSMessageResponse, SQSReceiveMessageResponse
from lambda_utility.session import create_client


def remove_none(**kwargs: Any) -> dict:
    return {key: value for key, value in kwargs.items() if value is not None}


async def get_queue_url(
    queue_name: str,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> str:
    """Returns the URL of an existing Amazon SQS queue.

    :ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.get_queue_url
    :exception: SQS.Client.exceptions.QueueDoesNotExist
    """
    if client is None:
        client = create_client("sqs", config=config)

    async with client as client_obj:
        response = await client_obj.get_queue_url(QueueName=queue_name)
        return response["QueueUrl"]


async def send_message(
    queue_url: str,
    message_body: str,
    *,
    delay_seconds: Optional[int] = None,
    message_attributes: Optional[dict] = None,
    message_system_attributes: Optional[dict] = None,
    message_deduplication_id: Optional[str] = None,
    message_group_id: Optional[str] = None,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> SQSMessageResponse:
    """Delivers a message to the specified queue.

    :ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.send_message
    :exception: SQS.Client.exceptions.InvalidMessageContents
    :exception: SQS.Client.exceptions.UnsupportedOperation
    """
    if client is None:
        client = create_client("sqs", config=config)

    async with client as client_obj:
        result = await client_obj.send_message(
            **remove_none(
                QueueUrl=queue_url,
                MessageBody=message_body,
                DelaySeconds=delay_seconds,
                MessageAttributes=message_attributes,
                MessageSystemAttributes=message_system_attributes,
                MessageDeduplicationId=message_deduplication_id,
                MessageGroupId=message_group_id,
            )
        )

        return SQSMessageResponse(**result)


async def delete_message(
    queue_url: str,
    receipt_handle: str,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> None:
    """Deletes the specified message from the specified queue.

    :ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.delete_message
    :exception: SQS.Client.exceptions.InvalidIdFormat
    :exception: SQS.Client.exceptions.ReceiptHandleIsInvalid
    """
    if client is None:
        client = create_client("sqs", config=config)

    async with client as client_obj:
        await client_obj.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle,
        )


async def receive_message(
    queue_url: str,
    attribute_names: Optional[list[str]] = None,
    message_attribute_names: Optional[list[str]] = None,
    max_number_of_messages: Optional[int] = None,
    visibility_timeout: Optional[int] = None,
    wait_time_seconds: Optional[int] = None,
    receive_request_attempt_id: Optional[str] = None,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> SQSReceiveMessageResponse:
    """Retrieves one or more messages (up to 10), from the specified queue.

    :ref: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#SQS.Client.receive_message
    :exception: SQS.Client.exceptions.OverLimit
    """
    if client is None:
        client = create_client("sqs", config=config)

    async with client as client_obj:
        result = await client_obj.receive_message(
            **remove_none(
                QueueUrl=queue_url,
                AttributeNames=attribute_names,
                MessageAttributeNames=message_attribute_names,
                MaxNumberOfMessages=max_number_of_messages,
                VisibilityTimeout=visibility_timeout,
                WaitTimeSeconds=wait_time_seconds,
                ReceiveRequestAttemptId=receive_request_attempt_id,
            ),
        )
        return SQSReceiveMessageResponse(**result)
