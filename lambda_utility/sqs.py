from __future__ import annotations

__all__ = (
    "get_queue_url",
    "send_message",
)

from typing import Optional, Any

import aiobotocore
import botocore.client

from lambda_utility.schema import SQSMessageResponse
from lambda_utility.session import create_client


def remove_none(**kwargs: Any) -> dict:
    return {key: value for key, value in kwargs.items() if value is not None}


async def get_queue_url(
    queue_name: str,
    *,
    client: Optional[aiobotocore.session.ClientCreatorContext] = None,
    config: Optional[botocore.client.Config] = None,
) -> str:
    """
    :exceptions: botocore.errorfactory.QueueDoesNotExist
    """
    if client is None:
        client = create_client("sqs", config=config)

    async with client as client_obj:
        response = await client_obj.get_queue_url(QueueName=queue_name)
        print(response)
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
