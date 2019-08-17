from typing import Callable, Any

from functools import reduce


def pipe(f1: Callable, *fns: Callable) -> Callable:
    def args(*args: Any) -> str:
        return reduce(
            lambda res, fn: f"{res} | {fn()}",
            fns,
            f1(*args) or ""
        )

    return args
