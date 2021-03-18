from __future__ import annotations

__all__ = ("send_message",)

from typing import Union, Any

import slack_sdk


def send_message(
    token: str, channel: str, message: Union[str, list[dict[str, Any]]]
) -> slack_sdk.web.SlackResponse:
    """send a slack message

    :exception: slack_sdk.errors.SlackApiError
    """
    client = slack_sdk.WebClient(token=token)
    if isinstance(message, list):
        response = client.chat_postMessage(channel=channel, blocks=message)
    else:
        response = client.chat_postMessage(channel=channel, text=message)
    return response
