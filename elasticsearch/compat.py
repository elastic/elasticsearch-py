#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import asyncio
import inspect
import os
import sys
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from threading import Thread
from typing import Any, AsyncIterator, Callable, Coroutine, Iterator, Tuple, Type, Union

string_types: Tuple[Type[str], Type[bytes]] = (str, bytes)

DISABLE_WARN_STACKLEVEL_ENV_VAR = "DISABLE_WARN_STACKLEVEL"


def to_str(x: Union[str, bytes], encoding: str = "ascii") -> str:
    if not isinstance(x, str):
        return x.decode(encoding)
    return x


def to_bytes(x: Union[str, bytes], encoding: str = "ascii") -> bytes:
    if not isinstance(x, bytes):
        return x.encode(encoding)
    return x


def warn_stacklevel() -> int:
    """Dynamically determine warning stacklevel for warnings based on the call stack"""
    if os.environ.get(DISABLE_WARN_STACKLEVEL_ENV_VAR) in ["1", "true", "True"]:
        return 0
    try:
        # Grab the root module from the current module '__name__'
        module_name = __name__.partition(".")[0]
        module_path = Path(sys.modules[module_name].__file__)  # type: ignore[arg-type]

        # If the module is a folder we're looking at
        # subdirectories, otherwise we're looking for
        # an exact match.
        module_is_folder = module_path.name == "__init__.py"
        if module_is_folder:
            module_path = module_path.parent

        # Look through frames until we find a file that
        # isn't a part of our module, then return that stacklevel.
        for level, frame in enumerate(inspect.stack()):
            # Garbage collecting frames
            frame_filename = Path(frame.filename)
            del frame

            if (
                # If the module is a folder we look at subdirectory
                module_is_folder
                and module_path not in frame_filename.parents
            ) or (
                # Otherwise we're looking for an exact match.
                not module_is_folder
                and module_path != frame_filename
            ):
                return level
    except KeyError:
        pass
    return 0


@contextmanager
def safe_thread(
    target: Callable[..., Any], *args: Any, **kwargs: Any
) -> Iterator[Thread]:
    """Run a thread within a context manager block.

    The thread is automatically joined when the block ends. If the thread raised
    an exception, it is raised in the caller's context.
    """
    captured_exception = None

    def run() -> None:
        try:
            target(*args, **kwargs)
        except BaseException as exc:
            nonlocal captured_exception
            captured_exception = exc

    thread = Thread(target=run)
    thread.start()
    yield thread
    thread.join()
    if captured_exception:
        raise captured_exception


@asynccontextmanager
async def safe_task(
    coro: Coroutine[Any, Any, Any],
) -> "AsyncIterator[asyncio.Task[Any]]":
    """Run a background task within a context manager block.

    The task is awaited when the block ends.
    """
    task = asyncio.create_task(coro)
    yield task
    await task


__all__ = [
    "string_types",
    "to_str",
    "to_bytes",
    "warn_stacklevel",
    "safe_thread",
    "safe_task",
]
