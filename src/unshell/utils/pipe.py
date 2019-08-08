from typing import Callable, List, Any

from functools import reduce


def pipe(f1: Callable, *fns: List[Callable]) -> Callable:
    def args(*args: List[Any]) -> str:
        return reduce(
            lambda res, fn: f"{res} | {fn()}",
            fns,
            f1(*args) or ""
        )

    return args
