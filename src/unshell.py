from typing import Any, Callable
from type import Options, Script, Args, Commands

import inspect
import os

defaultOptions = Options(env={})


def Unshell(opt: Options = defaultOptions):
    def exec(script: Script, *args: Args) -> Any:
        assert_unshell_script(script)

        commands: Commands = script(*args)

        for command in commands:
            print(f"• {command}")

            res = os.system(command)

            print(res)

        return res

    return exec


def assert_unshell_script(fn: Callable) -> bool:
    if is_async_generator(fn):
        return True
    if is_generator(fn):
        return True

    raise TypeError('unshell: Invalid SCRIPT')


def is_generator(fn: Callable) -> bool:
    return inspect.isgeneratorfunction(fn)


def is_async_generator(fn: Callable) -> bool:
    return inspect.isgeneratorfunction(fn) and inspect.iscoroutinefunction(fn)
