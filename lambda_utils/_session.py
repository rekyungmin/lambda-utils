from __future__ import annotations

__all__ = (
    "get_session",
    "get_client",
    "get_resource",
)

import functools
from typing import Any

import boto3


@functools.lru_cache
def get_session(**config: Any):
    if config is None:
        config = {}
    return boto3.session.Session(**config)


def get_client(service: str, **config: Any):
    session = get_session(**config)
    return session.client(service)


def get_resource(service: str, **config: Any):
    session = get_session(**config)
    return session.resource(service)
