from __future__ import annotations

__all__ = (
    "LambdaMultiprocessingError",
    "LambdaMultiprocessing",
)

import functools
import json
import multiprocessing.connection
import re
import traceback
from typing import Any, Callable


def _get_traceback() -> list[str]:
    message = traceback.format_exc()
    unwanted_message = "Traceback (most recent call last):\n"
    if message.startswith(unwanted_message):
        message = message[len(unwanted_message) :]

    stack_trace = [
        each_file for each_file in re.split(r'\n(?=\s{2}File "[^\"]*")', message)
    ]
    return stack_trace


def _run_callable(connection, func: Callable[[], Any]) -> None:
    try:
        result = func()
        connection.send([True, result])
    except Exception as e:
        error_message = {
            "error_message": str(e),
            "error_type": type(e).__name__,
            "stack_trace": _get_traceback(),
        }
        connection.send([False, error_message])


class LambdaMultiprocessingError(Exception):
    def __init__(self, *error_results):
        self.error_results = error_results
        self.error_message = "\n\n".join(
            json.dumps(error_result, indent=4) for error_result in self.error_results
        )

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return self.error_message


class LambdaMultiprocessing:
    __slots__ = (
        "_processes",
        "_parent_connections",
    )

    _processes: list[multiprocessing.Process]
    _parent_connections: list[multiprocessing.connection.Connection]

    def __init__(self):
        self._processes = []
        self._parent_connections = []

    def clear(self) -> None:
        self._processes = []
        self._parent_connections = []

    def add_process(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        cb = functools.partial(func, *args, **kwargs)
        parent_conn, child_conn = multiprocessing.Pipe()
        process = multiprocessing.Process(target=_run_callable, args=(child_conn, cb))
        self._processes.append(process)
        self._parent_connections.append(parent_conn)

    def run(self) -> list[Any]:
        self._run_processes()
        results = self._get_results()
        self._join_processes()
        self.clear()
        return results

    def _run_processes(self) -> None:
        for process in self._processes:
            process.start()

    def _join_processes(self) -> None:
        for process in self._processes:
            process.join()

    def _get_results(self) -> list[Any]:
        results: list[tuple[bool, Any]] = [
            parent_connection.recv() for parent_connection in self._parent_connections
        ]
        fail_results = [result for is_success, result in results if not is_success]
        if fail_results:
            raise LambdaMultiprocessingError(*fail_results)

        return [result for _, result in results]
