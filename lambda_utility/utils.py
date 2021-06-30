from __future__ import annotations

__all__ = (
    "timeit_ctx_manager",
    "timeit_decorator",
    "round_number",
    "LambdaRuntimeError",
    "exception_handler",
)

import contextlib
import decimal
import functools
import time
import traceback
from typing import TypeVar, Any, cast, Optional, Callable, Literal

from lambda_utility.typedefs import LambdaContext


@contextlib.contextmanager
def timeit_ctx_manager(
    decimal_point_limit: Optional[int] = None, prefix: str = "", postfix: str = ""
):
    start = time.perf_counter()
    yield
    elapsed_time = time.perf_counter() - start
    if decimal_point_limit is None:
        print(prefix, elapsed_time, postfix, sep="")
    else:
        print(prefix, round(elapsed_time, decimal_point_limit), sep="")


F = TypeVar("F", bound=Callable[..., Any])


def timeit_decorator(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__!r} function: {elapsed_time:.4f} seconds")
        return result

    return cast(F, wrapper)


def round_number(
    number: float,
    ndigits: int = 0,
    round_method: Literal[
        "ROUND_DOWN",
        "ROUND_HALF_UP",
        "ROUND_HALF_EVEN",
        "ROUND_CEILING",
        "ROUND_FLOOR",
        "ROUND_UP",
        "ROUND_HALF_DOWN",
        "ROUND_05UP",
    ] = "ROUND_HALF_UP",
) -> float:
    precision = "." + ("0" * (ndigits - 1)) + "1" if ndigits > 0 else "1"
    return float(
        decimal.Decimal(str(number)).quantize(
            decimal.Decimal(precision), rounding=round_method
        )
    )


LambdaHandlerT = TypeVar("LambdaHandlerT", bound=Callable[[Any, LambdaContext], Any])


class LambdaRuntimeError(Exception):
    pass


def exception_handler(func: LambdaHandlerT) -> LambdaHandlerT:
    @functools.wraps(func)
    def wrapper(event: Any, context: LambdaContext) -> Any:
        try:
            return func(event, context)
        except Exception as e:
            raise LambdaRuntimeError(
                f"Request Id: {context.aws_request_id} Event: {event}\n"
                f"{traceback.format_exc()}"
            ) from e

    return cast(LambdaHandlerT, wrapper)
