from __future__ import annotations

__all__ = (
    "InvocationType",
    "invoke",
)

import enum
from typing import Any, Optional

from lambda_utility import _session


class InvocationType(enum.Enum):
    EVENT = "Event"
    REQUEST_RESPONSE = "RequestResponse"
    DRY_RUN = "DryRun"


def invoke(
    function_name: str,
    invocation_type: InvocationType,
    payload_json: str = "",
    *,
    session_config: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    if session_config is None:
        session_config = {}
    session = _session.get_client("lambda", **session_config)
    return session.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type.value,
        Payload=payload_json,
    )
